### Requirements
- Python 2.7
- PIP
- GCloud SDK

## Features to be added
### Security
- Firebase secrets into templates without being able to use inspect element to view the secrets.

## Deployment
```shell
git clone git@github.com:taghead/CC_Assignment_2.git
cd ./CC_Assignment_2/Backend
pip install -r requirements.txt -t lib
gcloud components install app-engine-python --quiet
gcloud components install app-engine-python-extras --quiet
gcloud components update
dev_appserver.py .\Frontend\app.yaml .\Backend\app.yaml
```

## Deployment
```shell
git clone git@github.com:taghead/CC_Assignment_2.git
cd ./CC_Assignment_2/Backend
pip install -r requirements.txt -t lib
gcloud components install app-engine-python --quiet
gcloud components install app-engine-python-extras --quiet
gcloud components update
gcloud app deploy .\Frontend\app.yaml .\Backend\app.yaml
```