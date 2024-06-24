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


// Define your API routes
$app->get('/hello/{name}', function ($request, $response, $args) {
    $name = $args['name'];
    $response->getBody()->write("Hello, $name");
    return $response;
});

$app->get('/altcha_challenge', function ($request, $response, $args) {
    global $my_altcha;
    $challenge = $my_altcha->createChallenge();
    $response->getBody()->write(json_encode($challenge));
    return $response;
});

$app->post('/submit_form', function (Request $request, Response $response, $args) {
    global $my_altcha;

    $do_print = false;

    $body = $request->getBody();
    parse_str($body, $params);

    if($do_print) {
        print("params: ");
        print_r($params);
    }

    //$parsedBody = $request->getParsedBody();
    $name = $params['username'] ?? null;
    $password = $params['password'] ?? null;
    $altcha = $params['altcha'] ?? null;



    // Process the form data (e.g., validate, store in database, etc.)
    $status = "error";
    if ($name && $password) {
        $status = "okay";

        $data = [
            'name' => $name,
            'password' => $password, // In real applications, do not return the password like this.
        ];

        $altcha_status = "invalid";
        // For example, just echoing the data back as JSON
        if($do_print) {
            print("Form data complete: status=$status, name=$name, password=$password\n");
        }

        if ($my_altcha->validPayload($altcha)) {
            $altcha_status = "valid";
        }

        if($do_print) {
            print("altcha_status : $altcha_status\n");
        }

        $enc_data =  json_encode($data);
        //$enc_altcha = json_encode($altcha); // This is still base 64 encoded, so not human readable.

        $response->getBody()->write("{ \"status\": \"$status\", \"altcha_status\": \"$altcha_status\", \"data\" : $enc_data, \"altcha\": \"$altcha\" }");
    } else {
        // If form data is missing
        if($do_print) {
            print("Form data incomplete: status=$status, name=$name, password=$password.\n");
        }
        $error = [
            'status' => $status,
            'error_message' => 'Name and password are required.',
        ];
        $response->getBody()->write(json_encode($error));
        return $response->withStatus(400); // Bad Request
    }

    return $response->withHeader('Content-Type', 'application/json');
});

// Run Slim app
$app->run();