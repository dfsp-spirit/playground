# altcha-test-python

## About

This is a  WIP demonstration of using Altcha in a web application with a Python backend.
It provides its own endpoint where clients can request a challenge, and has a server-side function to validate the challenge response computed by the client. This means it does NOT
require an Altcha API key.

## Installation

Make sure you have flask:

```sh
pip install flask
```

## Usage

Start the webserver with:

```sh
python app.py
```

You will need the PEM password, see below.

Then connect to [https://127.0.0.1:5000](https://127.0.0.1:5000). Note that we use HTTPS, not HTTP.


## Development info

The SSL cert was generated like this:

```sh
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365
```

### Passwords

The PEM pwd for the OpenSSL certificate is `altcha`. It is required when starting the web server.

