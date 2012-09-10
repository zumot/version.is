<?php
/******************************************************************************
 * Version Fetcher                                                            *
 ******************************************************************************/

// Load gist
$gist_id = '3691351';
$gist = file_get_contents('https://api.github.com/gists/'.$gist_id);
$gist = json_decode($gist, true);

$versions = array(); // Placeholder array

/******************************************************************************
 * Dynamicly fetch versions                                                   *
 ******************************************************************************/

// Second parameter gives us an assoc array instead of an object.
$sources = json_decode($gist['files']['sources.json']['content'], true);

foreach ($sources as $project => $source) {
  $version = 'Not Available'; // Version default value

  $filename = end(explode('/', $source));
  
  if (($filename == 'package.json') || ($filename == 'component.json')) {
    $info = json_decode(file_get_contents($source), true);
    $version = $info['version'];
  }

  if ($filename == 'grunt.js') {
    // TODO: This regex could need some love. 
    // Returns two matches (both version: 'x.x.x' and x.x.x)
    // can this be avoided?
    preg_match('/version: \'(.*)\'/', file_get_contents($source), $matches);
    $version = end($matches);
  }

  $versions[$project] = $version;
}

/******************************************************************************
 * Get versions manually from gist                                            *
 ******************************************************************************/

$manual = json_decode($gist['files']['versions.json']['content'],true);

foreach ($manual as $project => $version) {
  $versions[$project] = $version;
}

/******************************************************************************
 * Write result to file cache                                                 *
 ******************************************************************************/

$result = json_encode($versions);
file_put_contents('versions.json', $result);

echo '<pre>'.$result; // Output of the written data