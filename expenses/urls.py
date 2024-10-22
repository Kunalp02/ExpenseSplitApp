from django.urls import path
from .views import (
    RetriveUserExpenses,
    RetrieveOverallExpenses,
    DownloadBalanceSheet,
    AddExpenseView
)

urlpatterns = [
    path('expenses/', AddExpenseView.as_view(), name='add_expense'),
    path('expenses/user/', RetriveUserExpenses.as_view(), name='user_expenses'), 
    path('expenses/overall/', RetrieveOverallExpenses.as_view(), name='overall_expenses'),  
    path('expenses/balance-sheet/', DownloadBalanceSheet.as_view(), name='download_balance_sheet'),
]
