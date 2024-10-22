from rest_framework import serializers
from .models import User, Split, Expense

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'mobile']


class SplitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Split
        fields = ['user', 'amount_owed']


class ExpenseSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)
    amounts_owed = serializers.ListField(
        child=serializers.FloatField(), write_only=True, required=False
    )

    class Meta:
        model = Expense
        fields = ['title', 'total_amount', 'split_method', 'participants', 'amounts_owed']

    def create(self, validated_data):
        participants = validated_data.pop('participants')
        split_method = validated_data.get('split_method').upper()
        amounts_owed = validated_data.pop('amounts_owed', [])

        # Validate expense data based on split method
        self.validate_expense(validated_data, participants, amounts_owed)

        # Create the expense
        expense = Expense.objects.create(**validated_data)
        expense.participants.set(participants)

        # Handle different split methods
        split_methods = {
            'EQUAL': self.handle_equal_splits,
            'EXACT': self.handle_exact_splits,
            'PERCENTAGE': self.handle_percentage_splits,
        }

        # call split method handling function for specified split method
        split_method_function = split_methods.get(split_method)
        if split_method_function:
            split_method_function(expense, participants, amounts_owed, validated_data['total_amount'])

        return expense

    # data validation
    def validate(self, data):
        split_method = data.get('split_method', '').upper()

        if split_method == 'EQUAL':
            data.pop('amounts_owed', None)  
        elif split_method in ['EXACT', 'PERCENTAGE']:
            amounts_owed = data.get('amounts_owed')
            if not amounts_owed:
                raise serializers.ValidationError({
                    'amounts_owed': 'This field is required for exact or percentage splits.'
                })

        return data

    def validate_expense(self, validated_data, participants, amounts_owed):
        total_amount = validated_data.get('total_amount')
        split_method = validated_data.get('split_method', '').upper()

        if total_amount <= 0:
            raise serializers.ValidationError("Total amount must be greater than zero.")
        if not participants:
            raise serializers.ValidationError("At least one participant must be provided.")

        if split_method in ['EXACT', 'PERCENTAGE'] and len(amounts_owed) != len(participants):
            raise serializers.ValidationError("Amount owed must match the number of participants.")

        if split_method == 'PERCENTAGE' and sum(amounts_owed) != 100:
            raise serializers.ValidationError("Total percentage must equal 100.")

    # to optimize performance in case of large data I preferred to use bulk create
    def handle_equal_splits(self, expense, participants, _, total_amount):
        amount_per_user = total_amount / len(participants)
        splits = [Split(expense=expense, user=user, amount_owed=amount_per_user) for user in participants]
        Split.objects.bulk_create(splits)

    def handle_exact_splits(self, expense, participants, amounts_owed, _):
        splits = [
            Split(expense=expense, user=user, amount_owed=amount)
            for user, amount in zip(participants, amounts_owed) if amount >= 0
        ]
        if len(splits) != len(participants):
            raise serializers.ValidationError("All amounts must be non-negative.")
        Split.objects.bulk_create(splits)

    def handle_percentage_splits(self, expense, participants, percentages, total_amount):
        splits = [
            Split(expense=expense, user=user, amount_owed=(percentage / 100) * total_amount)
            for user, percentage in zip(participants, percentages)
        ]
        Split.objects.bulk_create(splits)
