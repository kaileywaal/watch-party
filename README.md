# Weather Wars Application

## Application Testing

This application was built for CSCA-5028 (Applications of Software Architecture for Big Data). The following is an explanation of what is included in the project, outlined according to the project rubric.

### Web application basic form, reporting

- Built in Flask. I chose Flask because it is a simple UI that does not require any dynamic interactions (in which case I would have used a JavaScript library). Since it is simply reporting on data that has already been collected and analyzed, a simple UI with Flask made the most sense.
- Source code can be found in applications/web/app.py

### Data collection

- Data collection application collects historical weather data from [Open-Meteo API](https://open-meteo.com/en/docs/historical-weather-api/#start_date=2024-01-01&end_date=2024-04-08&hourly=&daily=daylight_duration,sunshine_duration&temperature_unit=fahrenheit&wind_speed_unit=mph&precipitation_unit=inch) and stores it in SQLite database.
- Source code can be found in applications/data_collector.py

### Data analyzer

- Data analyzer is triggered after new data is collected. It grabs any unanalyzed data and performs calculations to determine what percent of daylight hours were sunny for a given area. It stores this calculation in a SQLite database to allow quick + easy usage by the web application.
- Source code can be found in applications/data_analyzer.py

### Unit tests

- Unit tests written to ensure data analyzer and data collection work as expected.
- Tests are configured to run automatically on push for CI/CD through Github Actions. They can also be run manually via run_tests.py python script.
- All tests can be found in applications/tests folder.

### Data persistence any data store

- SQLite database for data persistence. Chosen because it is lightweight and this is a small-scale application that does not have need for additional complexity with hosting a separate database instance.
- SQLAlchemy as ORM to allow for database abstraction. Hypothetically, if there ever were a need to scale this application it would be easier to migrate.
- Database initialization code found in schema_setup.py. Interactions with data through DataGateway classes, found in components folder.

### Rest collaboration internal or API endpoint

- Data collection application collects historical weather data from [Open-Meteo API](https://open-meteo.com/en/docs/historical-weather-api/#start_date=2024-01-01&end_date=2024-04-08&hourly=&daily=daylight_duration,sunshine_duration&temperature_unit=fahrenheit&wind_speed_unit=mph&precipitation_unit=inch)

### Product environment

- Application is hosted on [Render](https://render.com)
- Can view live [here](https://watch-party-96bl.onrender.com)

### Integration tests

- Integration tests ensure data analyzer and data collection work together as expected.
- Tests are configured to run automatically on push for CI/CD through Github Actions. They can also be run manually via run_tests.py python script.
- All tests can be found in applications/tests folder.

### Using mock objects or any test doubles

- Mock objects and test doubles are utilized to emulate the behavior of external dependencies or components that the application interacts with.
- Can be found in tests, which are in the applications/tests folder

### Continuous integration

- Continuous integration using GitHub Actions, which is configured to run all tests on push.
- You can view the results of these tests [here](https://github.com/kaileywaal/weather-wars/actions)
- Configuration details can be found in .github/workflows/ci.yml

### Production monitoring instrumenting

- `/health` endpoint returns 200 OK when application is healthy
- Source found in applications/web/app.py

### Event collaboration messaging

### Continuous delivery
