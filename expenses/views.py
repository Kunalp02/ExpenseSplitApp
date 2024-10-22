from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import User, Split, Expense
from .serializers import ExpenseSerializer
import csv
from django.http import HttpResponse
from drf_yasg.utils import swagger_auto_schema

class AddExpenseView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
            request_body=ExpenseSerializer,
            responses={201: ExpenseSerializer, 400: 'Invalid data'},
            operation_summary="Add an expense",
            operation_description="Create a new expense with the specified details."
        )
    def post(self, request):
        serializer = ExpenseSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            expense = serializer.save(created_by=request.user)
            return Response(ExpenseSerializer(expense).data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RetriveUserExpenses(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        responses={200: ExpenseSerializer(many=True), 404: 'No expenses found'},
        operation_summary="Retrieve user expenses",
        operation_description="Get a list of expenses created by the authenticated user."
    )
    def get(self, request):
        user = request.user
        expenses = Expense.objects.filter(created_by=user)
        serializer = ExpenseSerializer(expenses, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    

from drf_yasg import openapi

class RetrieveOverallExpenses(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "total_expenses": openapi.Schema(type=openapi.TYPE_NUMBER),
                    "expenses_detail": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "title": openapi.Schema(type=openapi.TYPE_STRING),
                                "total_amount": openapi.Schema(type=openapi.TYPE_NUMBER),
                                "split_method": openapi.Schema(type=openapi.TYPE_STRING),
                                "participants": openapi.Schema(
                                    type=openapi.TYPE_ARRAY,
                                    items=openapi.Schema(type=openapi.TYPE_STRING)
                                ),
                            }
                        )
                    ),
                }
            ),
            404: 'No expenses found'
        },
        operation_summary="Retrieve overall expenses",
        operation_description="Get the total expenses for all users and detailed information about each expense."
    )
    def get(self, request):
        expenses = Expense.objects.all()

        if not expenses.exists():
            return Response({"message": "No expenses found."}, status=status.HTTP_404_NOT_FOUND)

        total_expenses = sum(expense.total_amount for expense in expenses)
        overall_expenses = {
            "total_expenses": total_expenses,
            "expenses_detail": [
                {
                    "title": expense.title,
                    "total_amount": expense.total_amount,
                    "split_method": expense.split_method,
                    "participants": [str(user) for user in expense.participants.all()]
                } for expense in expenses
            ]
        }

        return Response(overall_expenses, status=status.HTTP_200_OK)


class DownloadBalanceSheet(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        responses={200: 'A CSV file will be downloaded', 404: 'No expenses found for this user'},
        operation_summary="Download balance sheet",
        operation_description="Download a CSV file of all expenses created by the authenticated user."
    )
    def get(self, request):
        user = request.user
        expenses = Expense.objects.filter(created_by=user)

        if not expenses.exists():
            return Response({"message": "No expenses found for this user."}, status=status.HTTP_404_NOT_FOUND)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="balance_sheet_{user.id}.csv"'

        writer = csv.writer(response)
        writer.writerow(['Title', 'Total Amount', 'Split Method', 'Participants'])

        for expense in expenses:
            participants = ", ".join(str(user) for user in expense.participants.all())
            writer.writerow([expense.title, expense.total_amount, expense.split_method, participants])

        return response
