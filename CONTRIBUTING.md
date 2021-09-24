# Contributing to this repository

## Reporting Issues

Include the following information in your issue:

- Describe what you expected to happen.
- If possible, include a minimal reproducible example to help us identify the issue. This also helps ensure that the issue is not with your own code.
- Describe what actually happened.

## Submitting Patches

If there is not an open issue for what you want to submit, please open one for discussion before working on a PR. You can work on any issue that doesn't have an open PR linked to it or a maintainer assigned to it. These show up in the sidebar. No need to ask if you can work on an issue that interests you.

Include the following in your patch:

- Use Flake8 to format your code.
- Include tests if your patch adds or changes code. Make sure the test fails without your patch.
- Update any relevant docs pages and docstrings.
- Add an entry in `CHANGELOG.md`. Use the same style as the other entries.

### First time setup

- Download and install the [latest version of git](https://git-scm.com/downloads).
- Configure git with your username and email.

```
$ git config --global user.name 'your username'
$ git config --global user.email 'your email'
```

- Make sure you have a GitHub account.
- Fork the repo to your GitHub account by clicking the Fork button.
- Clone the main repository locally.

```
$ git clone https://github.com/KnightHacks/hackathon-2021-backend
$ cd flask
```

- Add your fork as a remote to push your work to. Replace `{username}` with your username. This names the remote "fork", the default Knight Hacks remote is "origin".

```
$ git remote add fork https://github.com/{username}/hackathon-2021-backend
```

- Create a virtualenv.

- Upgrade pip, wheel, and setuptools.

```
$ python -m pip install -U pip wheel setuptools
```

- Install the development dependencies

```
$ pip install -r requirements-dev.txt
```

### Start coding

<!-- WIP -->

### Running Development Server

- Download the [latest version of Docker and Docker Compose](https://docs.docker.com/get-docker/).

- Run the development compose stack

```
$ docker-compose -f docker-compose-dev.yml up
```

### Running the tests

```
$ python -m src test
```
