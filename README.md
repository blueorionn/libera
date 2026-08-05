# FLASK BOOKLIST

![Cover Page](booklist/assets/cover.png)

This project is a Flask-based web application that explores session authentication and middleware. The backend handles user authentication using Flask sessions, enforcing secure login/logout mechanisms, and applying middleware for request validation and logging. This setup provides a structured way to learn about user authentication, middleware functions, and frontend asset management in a Flask environment.

⚠️ This project is created solely for fun and learning

## TechStack

- Flask
- Tailwindcss
- MariaDB

## Database Setup

Required a **MySQL/MariaDB** database local or cloud.

Create the movie table and load data as specified in the `data/books.sql` file.

## User Creation

To create a user, use the script with the following options. **Before beginning, make sure to properly load all environment variables listed in the [Installation section](#installation).**

```bash
python scripts/register_user.py -fn [first_name] -ln [lastname] -u [username] -p [password] -r [role] 
```

**Valid user roles are `admin` and `user`.**

## Installation

### Prerequisites

- Python 3.11+
- pip (Python package installer)
- Nodejs
- npm

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/blueorionn/Flask-BookList.git
   cd Flask-BookList
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Export variables:

   ```bash
   export PYTHONDONTWRITEBYTECODE=1
   export FLASK_ENV="development"
   export SECRET_KEY="your-secret-key"
   export DB_URI="mysql://user:password@host:port/dbname"
   ```

   > `DB_URI` replaces the old `DB_HOST`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`,
   > and `DB_PORT` variables.  The old individual variables still work as a
   > fallback when `DB_URI` is not set.

5. Run the Flask app:

   ```bash
   python wsgi.py
   ```

6. Open the app in your browser at `http://127.0.0.1:8000/`.

## License

This project is released under the MIT License.
