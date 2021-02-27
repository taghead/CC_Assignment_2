


## Deployment and Testing Prerequisite
- Python 2.7
- PIP
- GCloud SDK

### Local Testing
```shell
git clone git@github.com:taghead/BP192-COSC2626-2020-Cloud-Computing-Assignment-2.git
cd ./CC_Assignment_2/Backend
pip install -r requirements.txt -t lib
gcloud components install app-engine-python --quiet
gcloud components install app-engine-python-extras --quiet
gcloud components update
dev_appserver.py .\Frontend\app.yaml .\Backend\app.yaml
```

### Deployment
```shell
git clone git@github.com:taghead/BP192-COSC2626-2020-Cloud-Computing-Assignment-2.git
cd ./CC_Assignment_2/Backend
pip install -r requirements.txt -t lib
gcloud components install app-engine-python --quiet
gcloud components install app-engine-python-extras --quiet
gcloud components update
gcloud app deploy .\Frontend\app.yaml .\Backend\app.yaml
```
