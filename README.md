# Turangga, a lightweight URL Shorterner
Turangga is a simple and lightweight URL Shortener service. It comes with API Server and Line@ bot webhooks. You can modify this service easily. The name "Turangga" means "horse" in Sundanese, hoping that this will serve as fast as possible.

To see this program in action, just add Turangga (@ejg5044b) at Line [![Turangga (@ejg5044b)]("https://scdn.line-apps.com/n/line_add_friends/btn/en.png)](https://line.me/R/ti/p/%40ejg5044b)


## Requirements
- Python 3.
- All libraries in `requirements.txt`.

## Installing
- Make sure that you have installed Python 3.
- Install the dependencies with `pip install -r requirements.txt`.
- Create a MySQL database based on `database.sql`.
- (Optional) Make a Line@ bot account.
- Make a file named `myconfig.py` with these configuration and complete it with the previously created MySQL database and optionally Line@ bot account.
```python
baseurl = ''    # Your resolver base URL. The default is 'http://yourdomain.com/s', but can be modified in app.py when stating url prefix for resolver Blueprint

channel_access_token = '' # You can get it at Line@ developer tool
channel_secret = '' # You can get it at Line@ developer tool

host = ''       # Your MySQL host
user = ''       # Your MySQL user
password = ''   # Your MySQL password
database = ''   # Your MySQL database name

if baseurl[len(baseurl)-1] != '/':
    baseurl += '/'

```
- Point your Line@ bot account webhooks to https://your.domain/line. (You should use SSL to use Line@ bot.)
## Running
- Run `python app.py`

The default port for this server is 5000. You can change it by modifying the `app.py` file
