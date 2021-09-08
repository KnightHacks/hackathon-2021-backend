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

1. Install the requirements. It is suggested that you use a Python virtual environment.

`pip install -r requirements.txt`

2. Run the server

`python -m src run --port=5000`

3. Access Swagger API Documentation

Type `localhost:5000/apidocs` in your browser


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

## Contributing

For guidance on setting up a development environment and how to make a contribution, see the [contributing guidelines](./CONTRIBUTING.md)

## Links

- Website: [https://knighthacks.org](https://knighthacks.org)
- LinkTree: [https://knighthacks.org/linktree](https://knighthacks.org/linktree)
- Discord: [https://discord.gg/Kv5g9vf](https://discord.gg/Kv5g9vf)
- Instagram: [https://www.instagram.com/knighthacks/](https://www.instagram.com/knighthacks/)
- Facebook: [https://www.facebook.com/KnightHacks/](https://www.facebook.com/KnightHacks/)
- Twitter: [https://twitter.com/KnightHacks/](https://twitter.com/KnightHacks/)
- Linkedin: [https://www.linkedin.com/company/knight-hacks/](https://www.linkedin.com/company/knight-hacks/)
- TikTok: [https://www.tiktok.com/@knight.hacks](https://www.tiktok.com/@knight.hacks)
