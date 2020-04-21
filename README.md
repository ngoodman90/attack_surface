## Environment Setup

* Python 3.6+ must be installed along with pip 
* Create a virtualenv


## Installation

Run the following install commands at the project root. Make sure the virtual env is activated.

```bash
$ pip install -r requirements.txt
```

## Running the server
Fill init_data.json with data.
Then run:
```bash
$ python main.py
```

## Restart the server
```bash
$ kill -9 $(lsof -i TCP:8000 | grep LISTEN | awk '{print $2}')
$ python main.py
```
