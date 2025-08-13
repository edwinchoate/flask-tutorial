# flaskr

The [tutorial project](https://flask.palletsprojects.com/en/stable/tutorial/) on [flask.palletsprojects.com](https://flask.palletsprojects.com)

## Create venv (if necessary)

```shell
$ python3 -m venv .venv
```

## Activate venv

Unix

```shell
$ source .venv/bin/activate
(.venv) $
```

Windows

```shell
> .venv/Scripts/activate
(.venv) >
```

## Install dependencies

```shell
(.venv) $ pip install -r requirements.txt
```

## Initialize the database

```shell
(.venv) $ flask --app flaskr init_db
```

## Run app

```shell
(.venv) $ flask --app flaskr run
```

```shell
(.venv) $ flask --app flaskr run --debug
```
