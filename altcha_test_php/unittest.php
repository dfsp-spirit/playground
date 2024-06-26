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

$salt = "7ad13678cadcea5e568b104a";
$number = 17; # the solution, this is what the JS client needs to compute als POW.
$challenge = $my_altcha->createChallenge($salt, $number);



if ($challenge["algorithm"] != "SHA-256") { throw new Exception("Invalid algorithm " . $challenge['algorithm'] . "."); }
$num_asserts_okay++;
if ($challenge["salt"] != $salt) { throw new Exception("Invalid salt " . $challenge['salt'] . "."); }
$num_asserts_okay++;
if ($challenge["challenge"] != "88bc1d7c2f91e30eb1b4992030a22858b6ccad51c8047abab1ed8648aa8a0dd2") { throw new Exception("Invalid challenge " . $challenge['challenge'] . "."); }
$num_asserts_okay++;
if ($challenge["signature"] != "48a60ba70fa7560d83b8173a694c9f74728e551ca8fd40e22688e20817108c34") { throw new Exception("Invalid signature " . $challenge['signature'] . "."); }
$num_asserts_okay++;

$client_response = $challenge; // You would get the response from the client, submitted with the form contents.
$client_response["number"] = $number;
$encoded_response = base64_encode(json_encode($client_response));

$is_valid = $my_altcha->validPayload($encoded_response);

if ($is_valid != true) { throw new Exception("Expected valid payload."); }
$num_asserts_okay++;

print("All okay, $num_asserts_okay checks passed.\n");

