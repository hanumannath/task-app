# task-app
This is a simple task creating app that uses jwt for authentication

## Routes
/register: registration page.
/login: login page.

/api/home: task home page where all your tasks will be visible and you can add, edit, and delete any task also here, this page will not be accessible without login as it reqires jwt token.

/api/update/<task:id>: here you can edit a perticular task.

/api/delete/<task:id.: here you can delete a particular task.

## Database: SQLite

## Logs: logs are saved in app.log file
