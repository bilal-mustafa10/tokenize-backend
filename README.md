# Tokenize Backend

## Overview

This project is a Flask-based API backend designed to handle user authentication, AI-generated smart contracts, error management, and user data. The application is structured into several blueprints for modularity and clarity.

### Blueprints

- **`auth`**: Manages user registration and authentication processes.
- **`users`**: Handles user-related requests and operations.
- **`ai`**: Manages requests related to AI-generated smart contracts.
- **`smart_contract`**: Handles data-related requests for smart contracts.
- **`errors`**: Manages error handling across the application.

## Prerequisites

- Python 3.6+
- [Virtualenv](https://virtualenv.pypa.io/en/stable/installation/)

## Setup

Creating a virtual environment is recommended to manage dependencies and avoid conflicts with other projects. To create and activate a virtual environment, run:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install Dependencies

Once the virtual environment is activated, install the required packages:

```bash
pip install -r requirements.txt
```

This will install all necessary dependencies within your virtual environment.

## Running the Application

To start the Flask application, use the following command:

```bash
flask run
```

By default, the application will be accessible at `http://127.0.0.1:5000/`.


⚠️ **Warning**: The `.env` file contains sensitive API keys and configuration settings intended solely for supervisor testing purposes. This file includes private information that should not be shared or exposed publicly. Ensure it is kept secure and confidential at all times.


Ensure you have test dependencies installed, which are typically listed directly in `requirements.txt`.

### I verify that I am the sole author of the programmes contained in this archive, except where explicitly stated to the contrary

### Bilal Mustafa Sheikh

### 06-08-2024