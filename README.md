# Version.is

Single-page app and API for version checking of Open Source projects.

## Origin

This is the result of a [lazyweb-request](https://github.com/h5bp/lazyweb-requests/issues/96 "Issue #96: www.version.is Get latest version of Open Source projects.") by [@higgo](https://github.com/higgo "higgo").

## Data Source

Data is pulled in from the [version.is-sources](https://github.com/gustavnikolaj/version.is-sources) repo. The readme contains additional information.

## Try it

An early implementation of the api is available at [version-is.appspot.com](http://version-is.appspot.com "version.is at Google App Engine").

## Usage

Get a list of all projects monitored and their current version:
```
GET http://version.is/projects
```

Get the version of a single project:
```
GET http://version.is/<project_name>
```

The response can be delivered in 3 different formats; text/html, text/plain, application/json. You can specify the format using the querystring like this:
```
GET http://version.is/projects?format=<html|plain|json>
GET http://version.is/<project_name>?format=<html|plain|json>
```

Another way to specify the format, is using HTTP-Accept Headers. Consider the below example of fetching current jquery version in json format with curl in a terminal:
```
curl -i -H "Accept: application/json" "http://version.is/jquery"
```
Note that formats defined in the querystring overrules the HTTP-Accept header.


If you request the json format, you can specify a callback for JSONP, like this:
```
GET http://version.is/<project_name>?format=json&callback=<callbackFunctionName>
```

## Running it locally

If you want to poke around the code and run it locally, all you need to do is to install the [Google App Engine SDK for Python](https://developers.google.com/appengine/downloads#Google_App_Engine_SDK_for_Python "Google App Engine SDK for Python").

When you have installed the SDK, you clone the repo into a local folder, and "Add Existing Application..." from the app menus in the SDK. When that is done, you can run the app from within the SDK interface.

To build the local database, you just have to visit http://localhost:8080/tasks/get-versions in your browser. When having an empty database, it will take about 5 minutes at the moment. This will increase with the size of the sources repo. You can follow the progress of the task in the Logs, accessed from the SDK interface.