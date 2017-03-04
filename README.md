# Turangga, a lightweight URL Shorterner
Turangga is a simple and ligthweight API Server and Resolver for URL Shorterner. The name "Turangga" means "horse" in Sundanese, hoping that this will serve as fast as possible.

## Requirements
- Python 3.
- All libraries in `requirements.txt`.

## Installing
- Make sure that you have installed Python 3.
- Install the dependencies with `pip install -r requirements.txt`.
- Create a MySQL database based on `database.sql`.
- Make a file named `myconfig.py` with these configuration and complete it with the previously created MySQL database.
```python
baseurl = ''    # Your resolver base URL. The default is 'http://yourdomain.com/s', but can be modified in app.py when stating url prefix for resolver Blueprint

host = ''       # Your MySQL host
user = ''       # Your MySQL user
password = ''   # Your MySQL password
database = ''   # Your MySQL database name

if baseurl[len(baseurl)-1] != '/':
    baseurl += '/'

```

## Running
- Run `python app.py`

The default port for this server is 5000. You can change it by modifying the `app.py` file
