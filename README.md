apt install python3
pip install --upgrade setuptools
pip install --upgrade gcloud
pip install -t lib pyrebase
https://medium.com/@hiranya911/firebase-using-the-python-admin-sdk-on-google-cloud-functions-590f50226286

Deployment
dev_appserver.py Frontend/app.yaml Backend/app.yaml
gcloud app deploy .\Backend\index.yaml