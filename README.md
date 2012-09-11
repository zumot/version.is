# Version.is

Single-page app and API for version checking of Open Source projects.

# Origin

This is the result of a [lazyweb-request](https://github.com/h5bp/lazyweb-requests/issues/96 "Issue #96: www.version.is Get latest version of Open Source projects.") by [@higgo](https://github.com/higgo "higgo").

# Data Source

Data is pulled in from the gist below and cached on the server.

https://gist.github.com/3697931

The list consists of a key/value pair, ala projectname and github username or orginasation slash repo name. For jQuery this would be jquery=jquery/jquery and for backbone.js it would be backbone=documentcloud/backbone.

It pulls the version data from git tags via the GitHub API. Information about the individual tags will be stored in GAE Datastore, to lessen the load on the API.

The current versions are stored as a list in memcache to enable quick access.

# Try it

An early implementation of the api is available at [version-is.appspot.com](http://version-is.appspot.com "version.is at Google App Engine").

# Usage

Get a list of all projects monitored and their current version:
```
GET http://version.is/projects
```

Get the version of a single project
```
GET http://version.is/<project_name>
```

If you want a JSON formatted response, append `/json` to the request. If you want JSONP response add `/json?callback=CallbackFunctionName`.