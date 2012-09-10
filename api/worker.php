<?php

$versions = array();

$sources = json_decode(file_get_contents('version_sources.json'), true);

foreach ($sources as $project => $source) {
  $version = 'N/A';

  $filename = end(explode('/', $source));
  
  if ($filename == 'package.json') {
    $info = json_decode(file_get_contents($source), true);
    $version = $info['version'];
  }

  if ($filename == 'grunt.js') {
    // This regex could need some love. 
    // Returns two matches (both version: 'x.x.x' and x.x.x) - can this be avoided?
    preg_match('/version: \'(.*)\'/', file_get_contents($source), $matches);
    $version = end($matches);
  }

  $versions[$project] = $version;
}

$result = json_encode($versions);
file_put_contents('versions.json', $result);

echo '<pre>'.$result;