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

$algo = "SHA-256";
$secret_key = "bananeinderbirne";
$my_altcha = new Altcha($algo, $secret_key, 1, 100);


// ---- API routes -----

// Endpoint where a client can request an Altcha challenge.
$app->get('/altcha_challenge', function ($request, $response, $args) {
    global $my_altcha;
    $challenge = $my_altcha->createChallenge();
    $response->getBody()->write(json_encode($challenge));
    return $response;
});


// Form submission handler. This gets called when the user hits the Submit button on
// the `form.html` page.
// It checks whether the form data is complete (required fields filled out), and
// whether the returned Altcha response is valid. It does not check for or protect against replay attacks.
$app->post('/submit_form', function (Request $request, Response $response, $args) {
    global $my_altcha;

    $body = $request->getBody();
    parse_str($body, $params);

    //$parsedBody = $request->getParsedBody();
    $name = $params['username'] ?? null;
    $password = $params['password'] ?? null;
    $altcha_raw = $params['altcha'] ?? null; // still base64 encoded.
    $altcha_json = base64_decode($altcha_raw);  // decoded altcha as JSON
    $altcha_str = json_decode($altcha_json, true);  // decoded altcha as string


    // Process the form data (e.g., validate, store in database, etc.)
    $form_filled_status = "error";  // this status describes whether all required form fields were filled out.
    if ($name && $password) {
        $form_filled_status = "okay";

        $data = [
            'name' => $name,
            'password' => $password, // In real applications, do not return the password like this.
        ];

        $altcha_status = "invalid";
        // For example, just echoing the data back as JSON

        if ($my_altcha->validPayload($altcha_raw)) {
            $altcha_status = "valid";
            $enc_data =  json_encode($data);
            $response->getBody()->write("{ \"form_filled_status\": \"$form_filled_status\", \"altcha_status\": \"$altcha_status\", \"data\": $enc_data, \"altcha_raw\": \"$altcha_raw\", \"altcha\": $altcha_json }");  // Don't roll your own JSON, they told us in school.
        } else {
            $error = [
                'form_filled_status' => $form_filled_status,
                'altcha_status' => $altcha_status,
                'error_message' => 'Altcha captcha response invalid.',
            ];
            $response->getBody()->write(json_encode($error));
            return $response->withStatus(400); // Bad Request
        }

    } else {
        // If form data is missing
        $error = [
            'form_filled_status' => $form_filled_status,
            'error_message' => 'Name and password are required.',
        ];
        $response->getBody()->write(json_encode($error));
        return $response->withStatus(400); // Bad Request
    }

    return $response->withHeader('Content-Type', 'application/json');
});

// Run Slim app
$app->run();