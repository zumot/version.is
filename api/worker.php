<?php

$versions = array();

$sources = json_decode(file_get_contents('version_sources.json'), true);

foreach ($sources as $project => $source) {
  $info = json_decode(file_get_contents($source), true);
  $version = 'N/A';

  $filename = end(explode('/', $source));

  if ($filename == 'package.json') {
    $version = $info['version'];
  }
  $versions[$project] = $version;
}

$result = json_encode($versions);
file_put_contents('versions.json', $result);

echo '<pre>'.$result;