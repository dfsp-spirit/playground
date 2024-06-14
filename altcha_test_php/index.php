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
    $parsedBody = $request->getParsedBody();
    $name = $parsedBody['name'] ?? null;
    $password = $parsedBody['password'] ?? null;
    $altcha = $parsedBody['altcha'] ?? null;

    // Process the form data (e.g., validate, store in database, etc.)
    if ($name && $password) {
        // For example, just echoing the data back as JSON
        $data = [
            'name' => $name,
            'password' => $password, // In real applications, do not return the password like this.
        ];
        $response->getBody()->write("{ data :" + json_encode($data) + ", altcha: " + json_encode($altcha) + " }");
    } else {
        // If form data is missing
        $error = [
            'error' => 'Name and password are required.',
        ];
        $response->getBody()->write(json_encode($error));
        return $response->withStatus(400); // Bad Request
    }

    return $response->withHeader('Content-Type', 'application/json');
});

// Run Slim app
$app->run();