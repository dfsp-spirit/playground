<?php
use Slim\Factory\AppFactory;

require __DIR__ . '/vendor/autoload.php';

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

// Run Slim app
$app->run();