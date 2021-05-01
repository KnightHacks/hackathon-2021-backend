# Knight Hacks 2021 Backend

Backend server for Knight Hacks '21

## Contents

- [QuickStart](#quickstart)
- [Backend Environment Variables](#backend-environment-variables)
- [Testing](#testing)


## QuickStart

**Requirements:**

- MongoDB Server
- Python 3.9

1. Install the requirements.

`pip install -r requirements.txt`

2. Run the server

`python -m src run --port=5000`


## Backend Environment Variables

These are the default values, feel free to change them.

```
APP_SETTINGS=src.config.ProductionConfig
MONGO_URI=mongo://localhost:27017/test
```


## Testing

1. Install the dev requirements.

`pip install -r requirements-dev.txt`

2. Run the tests

`python -m src test`
