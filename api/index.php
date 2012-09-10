<?php

$response = array(
  'message' => 'hello world!',
  'uri' => $_SERVER['QUERY_STRING']
);

echo json_encode($response);