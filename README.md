# Installation

Clone the repo:
```bash
$ git clone https://github.com/sharadmv/auto-fantasy.git
$ cd auto-fantasy
```

Create a Python 3 virtualenv:
```bash
$ virtualenv venv -p python3
$ source venv/bin/activate
$ pip install -r requirements.txt
```

Create a file called `keys.json` with the following contents:

```json
{
    "consumer_key": "dj0yJmk9SUx0VXZmUFFObkFTJmQ9WVdrOWFGQnNObUpDTlRZbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmeD0wZQ--",
    "consumer_secret": "4520f2bf292abde19885d941f0e07afbd0ff3f68"
}
```

# 
```bash
$ python check_position.py (WR|RB|QB|TE|DEF|W/R/T)
```
