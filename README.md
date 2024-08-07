# My Django Project

## Table of Contents
- [Project Description](#project-description)
- [Features](#features)
- [Technologies](#technologies)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [Contact](#contact)

## Project Description
My Django Project is a cinema booking application that allows users to view movie schedules, book tickets, and manage their profiles. Users can update their email and password, view their purchased tickets, and request refunds.

## Features
- User authentication and profile management
- View movie schedules and details
- Book tickets for available screenings
- Update email and password
- Refund purchased tickets

## Technologies
- Python
- Django
- JavaScript (jQuery)
- HTML/CSS
- Bootstrap (optional for styling)
- SQLite (default database)

## Installation
### Prerequisites
- Python 3.6+
- Django 3.0+

### Steps
1. Clone the repository
    ```bash
    git clone https://github.com/eleonora3145/my_django.git
    cd my_django
    ```
2. Create a virtual environment and activate it
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```
3. Install the required packages
    ```bash
    pip install -r requirements.txt
    ```
4. Apply the migrations
    ```bash
    python manage.py migrate
    ```
5. Create a superuser
    ```bash
    python manage.py createsuperuser
    ```
6. Start the development server
    ```bash
    python manage.py runserver
    ```

## Usage
1. Open your web browser and go to `http://127.0.0.1:8000/`.
2. Register a new user or login with an existing account.
3. View available movie schedules, book tickets, and manage your profile.

### Profile Management
- Update Email: Navigate to your profile page and update your email address.
- Change Password: Navigate to your profile page and change your password.
- View Tickets: View your purchased tickets and request refunds if necessary.

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

## Contact
For any inquiries or issues, please contact:
- Eleonora Krech at [krechkivska.eleonora@gmail.com](mailto:krechkivska.eleonora@gmail.com)
- GitHub: [eleonora3145](https://github.com/eleonora3145)


