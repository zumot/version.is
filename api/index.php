<?php

$response = array(
  'message' => 'hello world!',
  'uri' => $_SERVER['REQUEST_URI']
);

echo json_encode($response);