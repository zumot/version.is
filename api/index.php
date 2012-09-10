<pre><?php
$url = parse_url($_SERVER['REQUEST_URI']);
$url['path'] = explode('/', ltrim(rtrim($url['path'], '/'), '/'));
parse_str($url['query'], $url['query']);

print_r($url);

echo PHP_EOL;

$cache_buster = floor(time() / 100) * 100;

echo $cache_buster . PHP_EOL;

//$versions = apc_fetch('versions.json:'.$cache_buster);

if (!$versions) {
  echo 'get content' . PHP_EOL;

  $versions = json_decode(file_get_contents('versions.json'));
  //apc_store('versions.json:'.$cache_buster, $versions);
}

print_r($versions);

if (isset($versions->{$url[0]})) {
  $response = array(
    $url[0] => $versions[$url[0]]
  );
} else {
  $response = array(
    'error' => 'No match found'
  );
}

echo json_encode($response);