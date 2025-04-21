# Group Expense Splitter

A web application for managing shared expenses within groups, built with Django.

## Features

- Create groups for shared expenses
- Add expenses with detailed attributes
- Split expenses equally or in custom ratios
- Automatically calculate who owes whom
- Mark settlements as paid
- Support multiple currencies
- Export data in PDF or Excel format
- User registration and authentication
- Profile management

## Installation

1. Clone the repository:
```
git clone https://github.com/yourusername/expense-splitter.git
cd expense-splitter
```

2. Create a virtual environment and activate it:
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```
pip install -r requirements.txt
```

4. Run migrations:
```
python manage.py migrate
```

5. Initialize default data:
```
python manage.py initialize_data
```

6. Create a superuser:
```
python manage.py createsuperuser
```

7. Run the development server:
```
python manage.py runserver
```

8. Access the application at http://127.0.0.1:8000/

## Usage

1. Register a new account or log in
2. Create a group for your shared expenses
3. Invite friends to join your group
4. Add expenses and specify how they should be split
5. View the settlement summary to see who owes whom
6. Mark settlements as paid when money is exchanged
7. Export the data as needed

## Technologies Used

- Django
- SQLite (development) / PostgreSQL (production)
- Bootstrap
- JavaScript
- ReportLab (PDF generation)
- XlsxWriter (Excel generation)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Inspired by Splid and other expense splitting applications
- Built as a learning project for Django web development
