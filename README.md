# Serchie: Housing Finder

## Overview

Serchie is a Python-based housing finder application that connects tenants with landlords. It provides an intuitive interface for tenants to search for properties and for landlords to manage their listings.

## Features

- **User Roles**: Separate interfaces for tenants and landlords
- **Tenant Features**:
  - Search properties by type, location, and price range
  - View detailed property listings
- **Landlord Features**:
  - Secure login and signup system
  - Add, edit, and delete property listings
  - View all current listings
- **Database Integration**: MySQL database for storing user and property information
- **Security**: Password hashing for landlord accounts

## Requirements

- Python 3.x
- Tkinter (usually comes with Python)
- MySQL
- Additional Python packages:
  - mysql-connector-python
  - bcrypt
  - Pillow (PIL)

## Setup

1. Install the required packages:
   ```
   pip install mysql-connector-python bcrypt Pillow
   ```

2. Set up a MySQL database named `housing_db`.

3. Update the database connection details in the script:
   ```python
   self.conn = mysql.connector.connect(
       host='localhost',
       user='your_username',
       password='your_password',
       database='housing_db'
   )
   ```

4. Ensure you have a `logo.ico` file in the same directory as the script for the application icon.

## Usage

Run the script:
```
python serchie_housing_finder.py
```

### For Tenants:
1. Select the "Tenant" role.
2. Use the search interface to find properties based on type, location, and price range.
3. View the search results in the text area.

### For Landlords:
1. Select the "Landlord" role.
2. Sign up for a new account or log in to an existing one.
3. Use the dashboard to add new properties, view existing listings, edit property details, or delete listings.

## Contributing

Contributions to improve Serchie are welcome. Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Make your changes and commit (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature-branch`)
5. Create a new Pull Request

## License

[Add your chosen license here]

## Contact

[Your Name/Organization] - [Your Email]

Project Link: [https://github.com/Janleks/Bacani_JohnLex_ACP](https://github.com/Janleks/Bacani_JohnLex_ACP)
