<?php

// I could not get phpunit to install with the
// default PHP version shipped with Ubuntu 22.04 LTS,
// and I was not in the mood to research how to
// update PHP, no time for that fun. So this unit test
// does not use a test framework. Sorry for that.

require __DIR__ . '/vendor/autoload.php';

use Psr\Http\Message\ResponseInterface as Response;
use Slim\Factory\AppFactory;
use Slim\Psr7\Request;

$num_asserts_okay = 0; // Our unit test framework.

// Create Slim app
$app = AppFactory::create();

// Include CORS middleware
require __DIR__ . '/cors.php';
require __DIR__ . '/altcha.php';

$algo = "SHA-256";
$secret_key = "bananeinderbirne";
$my_altcha = new Altcha($algo, $secret_key, 1, 100);

$salt = bin2hex(random_bytes(12));
$number = 17; # the solution, this is what the JS client needs to compute als POW.
$challenge = $my_altcha->createChallenge($salt, $number);



assert($challenge["algorithm"] == "sha-256", "Expected algo sha-256.");
$num_asserts_okay++;

$client_response = $challenge; // You would get the response from the client, submitted with the form contents.
$client_response["number"] = $number;
$encoded_response = base64_encode(json_encode($client_response));

$is_valid = $my_altcha->validPayload($encoded_response);

assert($is_valid == true, "Expected valid payload.");
$num_asserts_okay++;

print("All okay, $num_asserts_okay checks passed.\n");

