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

The response can be delivered in 3 different formats; text/html, text/plain, application/json. You can specify the format like this:
```
GET http://version.is/projects?format=<html|plain|json>
GET http://version.is/<project_name>?format=<html|plain|json>
```

Another way to specify the format, is using HTTP-Accept Headers. Consider the below example of fetching current jquery version in json format with curl in a terminal:
```
curl -i -H "Accept: application/json" "http://version.is/jquery"
```
Note that formats defined in the querystring overrules the HTTP-Accept header.

You can also specify a format using a file extension. Note that this will override both querystring and HTTP-Accept header:
```
GET http://version.is/<project_name>.json
GET http://version.is/<project_name>.txt
```

If you request the json format, you can specify a callback for JSONP, like this:
```
GET http://version.is/<project_name>?format=json&callback=<callbackFunctionName>
GET http://version.is/<project_name>.json?callback=<callbackFunctionName>
```

## Running it locally

If you want to poke around the code and run it locally, all you need to do is to install the [Google App Engine SDK for Python](https://developers.google.com/appengine/downloads#Google_App_Engine_SDK_for_Python "Google App Engine SDK for Python").

When you have installed the SDK, you clone the repo into a local folder, and "Add Existing Application..." from the app menus in the SDK. When that is done, you can run the app from within the SDK interface.

To build the local database, you just have to visit http://localhost:8080/tasks/get-versions in your browser. When having an empty database, it will take up to about 10 minutes at the moment. This will increase with the size of the sources repo. You can follow the progress of the task in the Logs, accessed from the SDK interface.

The default datastore is located in a temporary folder, that once in a while and on restarts, will be cleared. To ensure that you do not have to rebuild the database after each restart of the application, you can move it into a file in the project folder. I use the name localdatastore (which is in the .gitignore of this repo) and the following Launch flags:

```
--datastore_path=/Users/gustav/Projects/version.is/localdatastore --use_sqlite
```

You would obviously want to change the path of the `--datastore_path` parameter. The --use_sqlite flag, makes it use sqlite instead of the default mysql, which removes the mysql dependency and makes the application start up faster. It might make the application perform slightly worse, but it should not be a concern when running it for testing purposes.

## Licence

Copyright &copy; 2012 Version.is | Code licensed under the [MIT License](http://opensource.org/licenses/MIT/).
