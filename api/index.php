<?php
header("Content-Type: application/json");

$url = parse_url($_SERVER['REQUEST_URI']);
$url['path'] = explode('/', ltrim($url['path'], '/')); // path to array

$project = $url['path'][0]; // Get project name

// if querystring is not empty check for a callback
if ($url['query']) {
  parse_str($url['query'], $url['query']);
  $callback = filter_var($url['query']['callback'], FILTER_SANITIZE_STRING);
} else {
  $callback = false;
}

// Cache buster to refresh APC cache every 100 secs.
$cacheTTL = floor(time() / 100) * 100;

// Try to fetch from APC
$versions = apc_fetch('versions.json'.$cacheTTL);

// If not in cache - then fetch and store
if (!$versions) {
  $versions = json_decode(file_get_contents('versions.json'), true);
  apc_store('versions.json'.$cacheTTL, $versions);
}


// If has data
if (isset($versions[$project])) {
  $response = array(
    'project' => $project,
    'version' => $versions[$project][0]
  );
}
// If not has data
else {
  $response = array(
    'error' => 'No match found for \''.$project.'\'',
    'project' => $project,
    'version' => ''
  );
}

// Returning the response
if ($url['query']['callback']) {
  // With Callback
  echo $url['query']['callback'] . '('.json_encode($response).');';
} else {
  // Without Callback
  echo json_encode($response);
}