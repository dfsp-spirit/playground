
## Installation

make sure you have `php` and `composer` installed, e.g. via apt: ```sudo apt install composer php```.

Then, in this directory:

```sh
composer install
```

to install deps.

## Start web server:

```sh
php -S localhost:8001
```

# Use

Now in browser, go to:

* http://localhost:8001/form.html to see the form protected with the captcha, or
* http://localhost:8001/altcha_challenge to get an Altcha challenge in JSON format (this is where the form gets it from)

When you click the *Submit* button in the form, you will be taken to the `form_submit` endpoint, which checks the challenge. See the file [index.php](./index.php) for the definition.


