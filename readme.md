# Expense Sharing Application

This API enables users to register, add expenses, and split costs among participants using various methods like equal, exact, or percentage-based splits. It also allows users to view and download a balance sheet of all expenses.

---

## Table of Contents

- [Setup](#setup)
- [Working](#working)
  - [User Registration](#user-registration)
  - [Adding Expenses](#adding-expenses)
  - [View User Expenses](#view-user-expenses)
  - [View Overall Expenses](#view-overall-expenses)
  - [Download Balance Sheet](#download-balance-sheet)
- [API Documentation](#api-documentation)

---

## Setup
1. First we have to create a virtual environment where all our packages will get installed.

```bash
python -m venv myvenv
```

2. Now, Activate the virtual environment
```bash
myvenv/Scripts/activate -> press tab and hit enter
```

3. Installation of all dependencies

```bash
python -m pip install -r requirements.txt
```

- incase if you missed any pacakge to install simply enter this command in terminal
```bash
pip install package_name
```

4. we have to migrate our database so the tables will get created.
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Run the server
```bash
python manage.py runserver
```

- Swagger Documentation for apis -> http://localhost:8000/swagger


## Working
## user-registration
- `/auth/register/` to register user make post request to this endpoint with following payload:

```json
{
  "email": "user1@example.com",
  "password": "user1",
  "password2": "user1",
  "name": "user1",
  "mobile": "123456"
}

```
## adding-expenses
- `/api/expenses/` To add an expense, make a POST request with the following payload:
```json

For equal split 
{
  "title": "Dinner",
  "total_amount": 100,
  "split_method": "EQUAL",
  "participants": [1, 2, 3]
}

for exact split
{
  "title": "Group Trip Expenses",
  "total_amount": 300.00,
  "split_method": "EXACT",
  "participants": [1, 2, 3],
  "amounts_owed": [100.00, 120.00, 80.00]
}

for percentage split
{
  "title": "Electricity Bill",
  "total_amount": 150.00,
  "split_method": "PERCENTAGE",
  "participants": [1, 2],
  "amounts_owed": [60, 40]
}

```

## view-user-expenses
## view-overall-expenses
## to download balance sheet
- `/api/expenses/user/` Make Get request to get list of user expenses 
- `/api/expenses/overall/` Make Get request to get list of overall expenses
- `api/expenses/balance-sheet/` To download balance sheet of expenses

## api-documentation
- Postman link where you can test the apis
[<img src="https://run.pstmn.io/button.svg" alt="Run In Postman" style="width: 128px; height: 32px;">](https://app.getpostman.com/run-collection/20244302-1a0a4713-582a-41d6-945e-964c92979480?action=collection%2Ffork&source=rip_markdown&collection-url=entityId%3D20244302-1a0a4713-582a-41d6-945e-964c92979480%26entityType%3Dcollection%26workspaceId%3D4fc25884-ecfc-4754-97b1-ead9597d1bc0)

## To Build and Run Docker Image of application
Open Docker Desktop in background
In vs code terminal enter following commands

```bash
docker build -t expense-sharing-app .

docker run -p 8000:8000 expense-sharing-app
```

## Test Cases
```bash
python manage.py test
```

