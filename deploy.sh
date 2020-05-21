#/bin/bash
# sudo chmod u=rwx ./deploy.sh
gcloud app deploy ./Backend/index.yaml ./Backend/app.yaml ./Frontend/app.yaml