# Niner Exchange

Niner Exchange is a platform enabling users to exchange or give away course materials they no longer need. The application serves to help UNC Charlotte students offload and acquire their course materials for the semester at a cheaper price than the traditional Barnes and Noble UNC Charlotte Bookstore or the Niner Course Pack. Individuals will be able to list their course materials from past semesters on the site for sale or exchange or search for their course materials that other students may have up for trade or sale. The users will then be able to contact the individual who has posted their goods for sale and then figure out an exchange that will benefit both parties involved. 

## Installation

### Requirements
- Python 3
- PostgreSQL
- DataGrip (optional, for database management)

### Steps

1. **Clone the repository:**
```sh
git clone https://github.com/SamEads/niner_exchange.git
```

2. **Navigate to the project directory:**
```sh
cd niner_exchange
```

3. **Install the necessary dependencies:**
```sh
pip install -r requirements.txt
```

4. **Set up the database:**

You can set up the database using either a headless method or DataGrip.

**Headless Method:**
- Ensure PostgreSQL is installed and running.
- Create a new database for the application.
- Execute the SQL script to set up the database schema:
    ```sh
    psql -U your_username -d your_database -f data/script.sql
    ```

**DataGrip Method:**
- Open DataGrip and register your PostgreSQL host in the Database Explorer.
- Access your database from the query console.
- Open the `data/script.sql` file in DataGrip.
- Run the script by pressing `Ctrl + Enter`.

5. **Set up the `.env` file with your database connection string:**
```sh
DB_CON_STR="your_database_connection_string_here"
```

6. **Run the application:**
```sh
flask run
```

## Updating the Repository

To update your local repository with the latest changes from the remote repository, follow these steps:

1. **Navigate to your project directory:**
```sh
cd niner_exchange
```

2. **Pull the latest changes from the remote repository:**
```sh
git pull origin main
```

3. **Install any new dependencies:**
```sh
pip install -r requirements.txt
```

4. **Run the application:**
```sh
flask run
```