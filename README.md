# Web App Instructions

## To run the web application locally:

```
export FLASK_APP=src/app.py
flask run
```

## To run in debug mode:

Note: running in debug mode will allow the appication to reload when saving changes without having to restart the server.

1. Add this to the src/app.py file (if it is not already there)

```
if __name__ == "__main__":
    app.run(debug=True)
```

2. From the root directory, run the app with the following command:

```
Python src/app.py
```
