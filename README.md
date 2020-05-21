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

apt install python3
pip install --upgrade setuptools
pip install --upgrade gcloud
pip install -t lib pyrebase

https://medium.com/@hiranya911/firebase-using-the-python-admin-sdk-on-google-cloud-functions-590f50226286
https://github.com/GoogleCloudPlatform/python-docs-samples/tree/master/appengine/standard/firebase/firenotes
https://cloud.google.com/appengine/docs/standard/python/authenticating-users-firebase-appengine

Deployment
dev_appserver.py .\Frontend\app.yaml .\Backend\app.yaml
gcloud app deploy .\Backend\index.yaml .\Frontend\app.yaml .\Backend\app.yaml

Flask==1.1.2
pyjwt==1.7.1
flask-cors==3.0.8
google-auth==1.15.0
requests==2.23.0
requests-toolbelt==0.9.1
