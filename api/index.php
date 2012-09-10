<pre><?php
$url = parse_url($_SERVER['REQUEST_URI']);
$url['path'] = explode('/', ltrim($url['path'], '/'));
parse_str($url['query'], $url['query']);

$cache_buster = floor(time() / 100) * 100;

echo $url['path'][0];

$versions = apc_fetch('versions.json:'.$cache_buster);

if (!$versions) {
  echo 'get content' . PHP_EOL;

  $versions = json_decode(file_get_contents('versions.json'));
  apc_store('versions.json:'.$cache_buster, $versions);
}

if (isset($versions->{$url['path'][0]})) {
  $response = array(
    $url['path'][0] => $versions[$url['path'][0]]
  );
} else {
  $response = array(
    'error' => 'No match found'
  );
}

echo json_encode($response);