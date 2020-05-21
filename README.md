## Requirements
Creates the following file and put in your firebase web app secrets:

[/app/templates/](/app/templates/)config.py
```python
firebase_config = {
          "apiKey": ##########################################,
          "authDomain": ###################################,
          "databaseURL": ##########################################,
          "projectId": #################################################,
          "storageBucket": #################################################,
          "messagingSenderId": ##########################################,
          "appId": ##########################################,
          "measurementId": ############################
}
```

### Todo 
- Firebase secrets into templates without being able to use inspect element to view the secrets.
https://medium.com/@hiranya911/firebase-using-the-python-admin-sdk-on-google-cloud-functions-590f50226286
https://github.com/GoogleCloudPlatform/python-docs-samples/tree/master/appengine/standard/firebase/firenotes
https://cloud.google.com/appengine/docs/standard/python/authenticating-users-firebase-appengine


Deployment
`gcloud app deploy .\Backend\index.yaml .\app\app.yaml`

Local Testing
```shell
    gcloud components install app-engine-python --quiet
    gcloud components install app-engine-python-extras --quiet
    gcloud components update
    gcloud init
dev_appserver.py .\Frontend\app.yaml .\Backend\app.yaml
```