<?php

echo $_SERVER['QUERY_STRING'].PHP_EOL;

$response = array(
  'message' => 'hello world!',
  'uri' => $_SERVER['QUERY_STRING']
);

echo json_encode($response);