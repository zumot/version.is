<pre><?php
$url = parse_url($_SERVER['REQUEST_URI']);

print_r($url);

echo PHP_EOL;

$cache_buster = floor(time() / 100) * 100;

echo $cache_buster . PHP_EOL;

$versions = apc_fetch('versions.json:'.$cache_buster);

if (!$versions) {
  echo 'get content' . PHP_EOL;
}

echo json_encode($response);