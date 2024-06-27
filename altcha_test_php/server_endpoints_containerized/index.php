<?php

require __DIR__ . '/vendor/autoload.php';

use Psr\Http\Message\ResponseInterface as Response;
use Slim\Factory\AppFactory;
use Slim\Psr7\Request;

// Create Slim app
$app = AppFactory::create();

// Include CORS middleware
require __DIR__ . '/cors.php';
require __DIR__ . '/altcha.php';

$algo = "sha-256";

//$secret_key = "bananeinderbirne";  // development only
$secret_key = getenv("ALTCHA_SERVER_KEY", true);  // production.

$my_altcha = new Altcha($algo, $secret_key, 1, 100);


// ---- API routes -----

// Endpoint where a client can request an Altcha challenge.
// Just fire a HTTP GET request. The challenge is served as a JSON object with fields 'algorithm', 'salt', 'challenge', and 'signature'.
$app->get('/altcha_challenge', function ($request, $response, $args) {
    global $my_altcha;
    $challenge = $my_altcha->createChallenge();
    $response->getBody()->write(json_encode($challenge));
    return $response;
});

// Endpoint where a client can validate an Altcha response.
// Pass the base64 encoded Altcha response as a string in the field 'altcha' (the contained JSON string must have fields 'algorithm', 'salt', 'challenge', 'signature', and 'number', where number is the result or prove of work.)
$app->get('/altcha_validate', function ($request, $response, $args) {
    global $my_altcha;

    $body = $request->getBody();
    parse_str($body, $params);

    $altcha_raw = $params['altcha'] ?? null; // base64 encoded.

    $altcha_status = "invalid";

    // Handle bad request
    if(is_null($altcha_raw)) {
        $error = [
            'altcha_status' => $altcha_status,
            'error_message' => 'Altcha captcha response in query parameter \'altcha\' is required.',
        ];
        $response->getBody()->write(json_encode($error));
        return $response->withStatus(400); // Bad Request
    }

    // Handle potentially valid requests.
    $altcha_json = base64_decode($altcha_raw);

    if ($my_altcha->validPayload($altcha_raw)) {
        $altcha_status = "valid";
        $response->getBody()->write("{ \"altcha_status\": \"$altcha_status\", \"altcha_raw\": \"$altcha_raw\", \"altcha\": $altcha_json }");  // Never roll your own JSON, they told us.
    } else {
        $error = [
            'altcha_status' => $altcha_status,
            'error_message' => 'Altcha captcha response invalid.',
        ];
        $response->getBody()->write(json_encode($error));
    }
    return $response;
});

// Run Slim app
$app->run();
