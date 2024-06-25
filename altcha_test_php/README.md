
# altcha-test-php

## About

This is a fully working demonstration of using Altcha in a web application with a PHP backend.
It provides its own endpoint where clients can request a challenge, and has a server-side function to validate the challenge response computed by the client. This means it does NOT
require an Altcha API key.


## Installation

Make sure you have `php` and `composer` installed, e.g. via apt: ```sudo apt install composer php```.

Then, in this directory:

```sh
composer install
```

to install deps.

Note on the PHP version: *This was tested with PHP 8.1.2, which is the version that ships with Ubuntu 22.04 LTS. If you have a different PHP version, the package versions in composer.lock may not work for you. In that case, you can delete `composer.lock` and then run ```composer install```.*


## Usage

First start web server in the repo dir:

```sh
php -S localhost:8001
```


Now in browser, go to:

* http://localhost:8001/form.html to see the form protected with the captcha, or
* http://localhost:8001/altcha_challenge to get an Altcha challenge in JSON format (this is where the form gets it from)

When you click the *Submit* button in the form, you will be taken to the `form_submit` endpoint, which checks the challenge. See the file [index.php](./index.php) for the definition.

## Tests

Run ```php unittest.php``` for tests.

