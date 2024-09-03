# ATM System 🏦

This is a command-line based ATM (Automated Teller Machine) system implemented in Python. It allows users to perform various banking operations such as depositing, withdrawing, transferring funds, checking balance, and viewing transaction history. Additionally, it includes a customer management system for creating and managing user accounts, cards, and personal information.

## Features

### ATM Operations 💰

- Add a new card by entering the card number and CVV
- Deposit cash into the account
- Withdraw cash from the account
- Transfer funds to another account
- Check account balance
- Recharge mobile number
- View transaction history (deposits, withdrawals, transfers)
- Quit the ATM system

### Customer Account Management 👤

- Sign up as a customer or employee
- Show account information
- Change CVV (Card Verification Value)
- Create new card
- Show card information
- Change account password
- Remove account
- Logout

## Prerequisites

- Python 3.x 🐍
- Inquirer library (`pip install inquirer`)
- Simple Chalk library (`pip install simple-chalk`)
- pycountry library (`pip install pycountry`)

## Usage

1. Clone the repository or download the source code. 📥
2. Navigate to the project directory. 📂
3. Run the `run.py` file using Python: `python run.py` 🚀
4. Follow the prompts to perform various ATM operations or customer account management tasks. 💻

## File Structure

- `run.py`: The main file containing the ATM system logic and user interface.
- `Customer.py`: Contains the customer account management logic and user interface.
- `Account.py`: Contains the sign-up and login functionality.
- `Card.py`: Contains the `Card` class for generating and managing card information.
- `backend/database.py`: Contains the `DataBaseUsage` class for handling data storage and retrieval in Firebase Firestore.
- `backend/effect.py`: Contains the `Effect` class for displaying progress bars and other visual effects.
- `app.py`: A file that demonstrates the usage of the `pycountry` library for displaying a list of countries.

## Dependencies

- `inquirer`: A Python library for creating interactive command-line user interfaces. 📋
- `simple_chalk`: A Python library for adding colors and styles to terminal output. 🌈
- `re`: The Python regular expression module for input validation. 🔍
- `abc`: The Python abstract base class module for defining abstract classes. 📖
- `datetime`: The Python module for working with dates and times. ⏰
- `pycountry`: A Python library for dealing with countries and currencies. 🌍
- `firebase_admin`: A Python library for interacting with Firebase services, including Firestore. 🔥

## Firebase Integration 🌐

This project utilizes Firebase Firestore as the backend database for storing and retrieving user data. Make sure to set up a Firebase project and download the appropriate service account credentials JSON file. Place the JSON file in the `backend` directory and update the file path in `database.py` if necessary.

## Contributing

Contributions are welcome! 🎉 If you find any issues or have suggestions for improvements, please open an issue or submit a pull request. 🛠️
