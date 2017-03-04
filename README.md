# Turangga, a lightweight URL Shorterner
Turangga is a simple and ligthweight API Server for URL Shorterner. The name "Turangga" means "horse" in Sundanese, hoping that this will serve as fast as possible.

## Requirements
- Python 3.
- All libraries in `requirements.txt`.

## Installing
- Make sure that you have installed Python 3.
- Install the dependencies with `pip install -r requirements.txt`.
- Create a MySQL database based on `database.sql`.
- Make a file named `myconfig.py` with these configuration and complete it with the previously created MySQL database.
```python
host = ''
user = ''
password = ''
database = ''
```

## Running
- Run `python app.py`

The default port for this server is 5000. You can change it by modifying the `app.py` file
