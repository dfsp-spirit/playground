<?php
use Slim\Factory\AppFactory;

require __DIR__ . '/vendor/autoload.php';

// Create Slim app
$app = AppFactory::create();

// Include CORS middleware
require __DIR__ . '/cors.php';

// Define your API routes
$app->get('/hello/{name}', function ($request, $response, $args) {
    $name = $args['name'];
    $response->getBody()->write("Hello, $name");
    return $response;
});

// Run Slim app
$app->run();