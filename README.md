<div align="center">

<img src="logo.jpg" alt="DevcodeTrek Bank Logo" width="150">

# PyQt5 Bank Management GUI

A desktop banking simulation developed with **Python**, **PyQt5**, **Pandas** and Excel-based local data storage.

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![PyQt5](https://img.shields.io/badge/GUI-PyQt5-41CD52?style=flat-square&logo=qt&logoColor=white)
![Pandas](https://img.shields.io/badge/Data-Pandas-150458?style=flat-square&logo=pandas&logoColor=white)
![Status](https://img.shields.io/badge/Status-Educational%20Project-C9A227?style=flat-square)

</div>

## Overview

This project demonstrates the core workflow of a desktop banking application through a graphical user interface. Users can create an account, sign in with their account number and password, manage their balance and perform common account operations.

Account data is stored locally in an Excel file generated automatically when the application starts for the first time.

## Features

- Create a new bank account
- Account number and password-based authentication
- Deposit and withdraw money
- View current balance
- Apply interest to accounts
- List account records
- Update account password
- Delete an account
- Sign out and return to the login screen
- Automatic local Excel data file generation
- Desktop interface built with PyQt5

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| PyQt5 | Desktop graphical interface |
| Pandas | Account data operations |
| OpenPyXL | Reading and writing Excel files |
| Microsoft Excel | Local demonstration data storage |

## Project Structure

```text
pyqt5-bank-management-gui/
├── bank_gui.py
├── logo.jpg
├── README.md
└── .gitignore
```

The application creates `bank_accounts.xlsx` locally at runtime. This generated file must remain excluded from version control.

## Installation

```bash
git clone https://github.com/Devcodetrek/pyqt5-bank-management-gui.git
cd pyqt5-bank-management-gui
python -m venv .venv
```

Activate the environment on Windows:

```powershell
.venv\Scripts\activate
```

Install the dependencies and run the application:

```bash
pip install PyQt5 pandas openpyxl
python bank_gui.py
```

## Data & Security Notice

This repository does not include account records. The application generates `bank_accounts.xlsx` locally at runtime.

This project is an educational banking simulation and is **not suitable for real financial operations**. A production system should use a secure database, password hashing, access controls, encryption, audit logging and server-side validation.

## Future Improvements

- Secure password hashing
- SQLite or PostgreSQL database integration
- Transaction history
- Account-to-account transfers
- Role-based administration
- Automated tests
- Packaged desktop releases

## Author

Developed by **Yiğit Erdoğan** under **DevcodeTrek**.

---

<div align="center">

**Educational desktop software project · DevcodeTrek**

</div>
