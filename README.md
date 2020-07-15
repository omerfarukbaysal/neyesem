# This simple app offers meal to your delight

## How to Run
Require [Python 3.5+](https://www.python.org/ftp/python/3.6.4/python-3.6.4.exe) installed.

### Fork and clone this repository to your local machine.
```
https://github.com/omerfarukbaysal/neyesem
```
### Install required libraries
`pip3 install -r requirements.txt`

### Run Flask
`run flask`

## Possible Errors And Solutions

### sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) no such table: users

- Open your Python Terminal and type:
`from neyesem import db, create_app`

Then type:
`db.create_all(app=create_app())`

### Could not import "project.project".
- Be sure you are in the same directory as the virtual environment.
- Then run flask again.
- If you got same error again, type this to your console:
`set FLASK_APP=neyesem`