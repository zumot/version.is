<?php
// Getting the URL
$url = parse_url($_SERVER['REQUEST_URI']);
// Exploding the path
$url['path'] = explode('/', ltrim($url['path'], '/'));
// Parsing the querystring
parse_str($url['query'], $url['query']);

// Cache buster to refresh APC cache every 100 secs.
$cache_buster = floor(time() / 100) * 100;

// Try to fetch from APC
$versions = apc_fetch('versions.json'.$cache_buster);

// If not in cache - then fetch and store
if (!$versions) {
  $versions = json_decode(file_get_contents('versions.json'), true);
  apc_store('versions.json'.$cache_buster, $versions);
}

// Project key
$project = $url['path'][0];

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