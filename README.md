To run locally:

```
export FLASK_APP=src/app.py
flask run
```

To run in debug mode, which will allow it to reload on changes without having to restart the server:

1. Add this to the src/app.py file

```
if __name__ == "__main__":
    app.run(debug=True)
```

2. Run the app with the following command:

```
Python src/app.py
```
