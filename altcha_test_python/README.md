Make sure you have flask:

```sh
pip install flask
```

Start the webserver with:

```sh
python app.py
```

The SSL cert was generated like this:

```sh
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365
```

The PEM pwd is `altcha`.

