<?php
use Slim\App;
use Tuupola\Middleware\CorsMiddleware;

return function (App $app) {
    $app->add(new CorsMiddleware([
        "origin" => ["*"], // You can restrict origins here e.g., "http://example.com"
        "methods" => ["GET", "POST", "PUT", "PATCH", "DELETE"],
        "headers.allow" => ["Authorization", "Content-Type"],
        "headers.expose" => [],
        "credentials" => true,
        "cache" => 0,
    ]));
};
