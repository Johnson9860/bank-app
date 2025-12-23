# JPMorgan Chase Online Banking Demo

A simple Flask-based online banking demonstration application themed as JPMorgan Chase.

## Features

- User authentication (login/logout)
- View account balance
- View account details
- Transaction history
- Transfer money between users
- Bill payment
- Cheques management
- Debit card management
- Credit card management
- Virtual card management
- Lifestyle services
- Book flights
- My flights management
- Movie ticket booking
- Event ticket booking
- Pension management
- Insurance policies
- Investment portfolio

## Database

This application uses SQLite database (`database.db`) to store user information and transaction history. The database is automatically created and initialized when the app starts.

## Demo Users

- Username: christopher98, Password: 986031, Balance: $900.00
- Username: user1, Password: pass1, Balance: $1000.00
- Username: user2, Password: pass2, Balance: $500.00

## Installation

1. Ensure you have Python 3.7+ installed.
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Running the Application

Run the Flask application:
```
python app.py
```

The application will start on `http://127.0.0.1:5000/`.

## Usage

1. Open your web browser and go to `http://127.0.0.1:5000/`.
2. Log in with one of the demo user credentials.
3. View your balance on the dashboard.
4. Transfer money to another user.
5. Log out when done.

## Security Note

This is a demo application themed as JPMorgan Chase and intentionally includes several security vulnerabilities for educational purposes to demonstrate common web application flaws. Do not use in production. Vulnerabilities include:

1. Hidden admin panel accessible without authentication
2. No validation for positive amounts (allows money duplication with negative values)
3. XSS vulnerability in bill payment descriptions
4. Plain text password storage
5. Hardcoded session secret key
6. Debug mode enabled (exposes sensitive information)

Use this demo to learn about web security best practices. It includes simulated vulnerabilities for educational purposes to demonstrate potential security risks.