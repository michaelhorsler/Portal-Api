# Portal-Api
DevOps Cohort - EPA Assessment Project


## Reference Paths and setup.

### Setup process for new Project.

Github repository:  https://github.com/michaelhorsler/Portal-Api.git

Github Actions CICD Pipeline: https://github.com/michaelhorsler/Portal-Api/actions/workflows/portal-api-ci-pipeline.yml

Docker Hub: https://hub.docker.com/repositories/michaelsminis

Azure Portal:  https://portal.azure.com/#home 

Login: (username)@bosch.com

Applied for Azure 60 day Sandbox license for project.
Prove if operation is suffiient or upgrade to Development license.

Azure details:
```
Portal-Api Resource Group: PortalApi
Azure Container Registry: portalapicontainer
Azure Web App: eng-portalapp
Azure Web App Service Plan: eng-portalapp-serviceplan
```
Azure published app domain: https://eng-portalapp.azurewebsites.net

JIRA Board for Project:
```
https://boschrexroth-team-vesb1xts.atlassian.net/jira/software/projects/SCRUM/boards/1/backlog
```

## Setup new project.
Create new repository within Github. i.e. portal-api.git.

https://github.com/michaelhorsler/portal-api.git

Open VS Code, clone repository. Select destination folder.

Readme.md for all updates and instructions.

```.gitignore``` to add all file extensions to not upload to Github.
```.env``` for all secret environment variables. Add .env extension to .gitignore.
```.env.json``` for json formatted variables - Azure WebApp.

Add ```poetry.toml``` and ```pyproject.toml``` to include all dependancy packages to install.

```Poetry Install``` runs and completes the package installation.

Additional folders include: templates for html page configurations. tests for later pytest files. data for data retrieval routines.

app.py is the main landing python script to execute as defined by flask variable. Routings can be including dependant upon request type.

flask_config.py includes secret-key definition to encrypt flask cookie data.

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.8+ and install Poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

You can check poetry is installed by running `poetry --version` from a terminal.

**Please note that after installing poetry you may need to restart VSCode and any terminals you are running before poetry will be recognised.**


## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.template` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/2.3.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.

## Running the App

Once the all dependencies have been installed, start the Flask app in development mode within the Poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app 'portalapi/app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 113-666-066
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

## Tests

Unit and Intgration tests will be included to prove operation via use of the Pytest module.
Mocking can provide expected dbase responses.

```
poetry add pytest
```
This downloads pytest to the project and updates pyproject.toml with the new dependancy. Pytest scans for all tests / files with the names test_*.py or *_test.py.

Configure pytest to look within the build folder to retrieve available tests within Visual Studio Code. All future tests will be scanned and added to the test list for execution.

TDD (Test Driven Development) can now drive the future expansion of the project.

Execute tests with the following command:
```
poetry run pytest
```
This will provide an output detailing the number of tests ran and their pass / fail results.

## Utilising Docker for containerisation - build and deployment

The Dockerfile in the root contains the full configuration for the container images to be built. This includes the base image to build upon, i.e. Python. Plus configuration options to build test and development environments taking into consideration different setups.
The sensitive configuration variables are imported from the .env file from the command line. An external port is exposed for viewing the app via the browser on your localhost:
```
docker run --env-file .env --publish 127.0.0.1:5000:5000 portalapi:prod
```
A Multi-stage build has been implemented to invoke either Production, Development or Test modes within the TodoApp. Built via the following commands to create seperate container VM's: 

```
$ docker build --target development --tag portalapi:dev .
$ docker build --target production --tag portalapi:prod .
$ docker build --target test --tag portalapi:test .
```
The .dockerignore file lists the files to not be included in the Docker build. I.e. secrets files: .env.


## Continuous Integration
Github Actions is used to create and manage the Continuous Integration pipeline. Visibility of the success and failure of the deployment pipeline and tests are easily monitored to ensure the successful operation and deployment of the Engineering Portal Api application.
 CI has many potential benefits, including reducing the risk of developers interfering with each others’ work and reducing the time it takes to get code to production.

The CI pipeline is defined within the following pipeline:

```
portal-api-ci-pipeline.yml
```
 This is stored within the ```.github\workflows folder```.
 E-mail notifications are setup within Github to alert Admin of failed CI pipeline deployments.


Login to DockerHub locally, build image and push to Docker.io ready for use within Azure:
```
docker Login
docker build --target production --tag michaelsminis/portalapi:prod .
docker push michaelsminis/portalapi:prod
```
Docker Image address:
```
https://hub.docker.com/r/michaelsminis/portalapi
```

## Deploy Application to Azure
Login to Azure Portal and Azure Container Registry (portalapicontainer)
```
az Login
az acr login --name portalapicontainer

docker build --target production --tag portalapicontainer.azurecr.io/portalapi:latest .
docker push portalapicontainer.azurecr.io/portalapi:latest
```
Pushed Azure container located in: portalapicontainer / Services / Repositories


Utilise account: michhors@bosch.com.

Resource-Group: PortalApi - BDO (DevOps Assessment).

Tenant: Bosch Group (DevOps Cohort)

Create an Azure AppService Plan:
```
az appservice plan create --resource-group PortalApi -n eng-portalapp-serviceplan --sku B1 --is-linux
```
Create an Azure WebApp:
```
az webapp create --resource-group PortalApi --plan eng-portalapp-serviceplan --name eng-portalapp --deployment-container-image-name portalapicontainer.azurecr.io/portalapi:latest
```
Assign App Settings via env.json:
```
az webapp config appsettings set -g PortalApi -n eng-portalapp --settings @env.json
```
Add the Webhook path retrieved from Azure WebApp / Deployment / Deployment Center. Enter via Gitbash: (Note: Webhook needs updating once WebApp has been created.)
```
curl -dH -X POST "https://$eng-portalapp:QbkRAs6ZrkittTqXNsNXM9GMpSFx5L92YNHFdlgeWrxzJ8leDmTZxkYgdkSe@eng-portalapp.scm.azurewebsites.net/api/registry/webhook"
```
Added Webhook to Azure / portalapicontainer / Services / Webhooks
To Update security on the container registry and allow admin access: portalapicontainer / Settings / Access Keys. Check Admin user for portalapicontainer username.

## Continuous Deployment

Advancing the CI pipeline to include CD (Continuous Delivery / Deployment) I am using Github Actions to publish the Production image direct to the Azure Container Registry and invoke the Azure Webhook to trigger the download of the latest image container onto the live application. Secrets are added to the Github repository (Portal-Api) Settings / Secrets and variables / Actions.

These include the Azure Webhook, Azure credentials, Registry username & Password, Resource Group in use.
The Azure credentials reflect the Admin account enabled within the Azure Container Registry with a unique access token to allow publication of containers to the ACR via the CICD pipeline creating a full CICD pipeline to deployment.

# Cosmos DB

## Setting up the MongoDb Integration

Pre-requisite: This app uses a Mongo Database for storing API request details and logging information. The database is hosted within the Azure engportalapi resource group.
```
secret.AZURE_COSMOS_DB_CLUSTER
```
Therefore a Mongodb database and connection string is required. These are referenced by Global Variables within `.env` - 
  MONGO_CONN_STRING, MONGODB.
These are required to achieve correct operation.

## Data Encryption in Azure Cosmos DB

All Azure Cosmos DB data is encrypted in transit (over the network) and at rest (nonvolatile storage), providing end-to-end encryption of our App data.

# Terraform Installation - Cloud Infrastructure as Code (IaC)

Binary installed into the working path.
Create main.tf with basic Azure resource data, variables stored within variables.tf and secrets protected in secrets.tfvars then initialise Terraform for project by:
```
az login
terraform init
```
In order to provide access for Terraform to provision resources within Azure, a Principle Service Account has been created by registering the Engineering Portal Api App with Microsoft EntraID and creating an App entry within the Bosch Active Directory (AD). A secret key and ID were created and assigned to a Contributor role for full provisioning.

Secret values have been secured within the secrets.tfvars file and need to be applied to the plan and application to allow logging into the Azure resources via the Principle Service Account.
To run and check terraform plan run:
```
terraform plan -var-file="secrets.tfvars"
terraform apply -var-file="secrets.tfvars"
```
If unable to execute and returns error code with subscription, check for any updates to the Azure Cli installation:
```
az extension --help
```
Install updates and log back into Azure Cli with az login.
Auto Upgrade can be configured with:
```
az config set auto-upgrade.enable=yes
```
## Transfer Terraform State to Azure Blob Storage

Transferring Terraform state from local file to Azure Blob Storage requires a Blob Storage Container to be created:
```
Either via Azure Portal:
Resource Group: PortalApi
Blob Storage: portalapistorageacc
Blob Container: portalapiblob

Via cli:
az storage account create --resource-group PortalApi --name portalapistorageacc --sku Standard_LRS --encryption-services blob

Create Blob Container via cli:
az storage container create --name portalapiblob --account-name portalapistorageacc
```

## Add Terraform to CICD Pipeline

To facilitate trusted login for Terraform, the Microsoft Entra Service Principle detailsa are added securely to the CICD Secrets within Github Actions as a JSON set. This equates to ClientID, ClientSecret, TenantID, SubscriptionID.
The following secrets are required:
```
AZURE_CREDENTIALS
```
Build variables transferred to Github secrets to allow reference from the CICD pipeline.
Variables Created:
```
SERVICE_PRINCIPLE_CLIENT_SECRET
MONGODBASE_CONN_STRING
MONGODBASE
DOCKER_SERVER_USR
DOCKER_SERVER_PWD
FLASK_APP
FLASK_DEBUG
SECRET_KEY
WEBSITES_PORT
```

# Container Orchestraion via Azure Kubernetes Service (AKS)

Additional files: service.yaml & deployment.yaml.
Setup for Azuze AKS service Cli:
```
az aks install-cli
```
To create the AKS Cluster:
```
az aks create --resource-group PortalApi --name portalapiAKSCluster --node-count 2 --node-vm-size standard_l8s_v3 --generate-ssh-keys --attach-acr portalapicontainer
```
Connecting to the AKS Cluster:
```
az login
az account set --subscription 50ef3721-085f-48dd-a4f1-d17b05980663
az aks get-credentials --resource-group PortalApi --name portalapiAKSCluster --overwrite-existing
```
AKS Cluster commands utilising kubectl:
```
kubectl get deployments --all-namespaces=true

kubectl get nodes - List cluster nodes (Set as 2 in deployment)
kubectl get pods	- List cluster pods
kubectl logs my-pod    - Retrieve the logs for a Pod called my-pod
kubectl describe pod my-pod  - Retrieve a description, including an error history, for my-pod 
kubectl delete pod <old-pod-name> --grace-period=0 --force  - force delete of pod
```
Add / upgrade latest version of k8s extension:
```
az extension add --upgrade --name k8s-extension
```

If pods fail to start from CICD, then interrogate logs and describe. If necessary delete pod to force re-creation.

Before applying AKS Configuration, ensure AKS secrets are added to the cluster to ensure variables are correctly applied to the pods. 'portalapisecret' becomes the referring store of secrets for the deployment.

```
kubectl create secret generic portalapisecret + list of secrets...
```

Reapply AKS configuration with:
```
kubectl apply -f AKS-Deployment.yaml
kubectl apply -f AKS-Service.yaml
```

ADD WEBHOOK TO AKS DEPLOYMENT!!!
# To-do

JIRA board created to monitor tasks and progress.

Cosmos Db added to Azure under free tier. Note: public access enabled but firewall rules need configuring to allow IP access.

Add Jason to Github repository to allow for pull-requests on deploying modifications. - Continuous Delivery and approved deployment.

Add metrics and monitoring against Serviceplan in Azure.

Add Kubernetes scaling to account for spikes in demand. Demonstrate scaling in use by way of simulated action? Temporary button within portal to provide multiple requests. View impact on Azure WebApp when it constant operation.

Add Terraform to manage Infrasturcture as code. (IaC)

Strip dependancies from VM. 

Review KSP's to hit and update accordingly. A4D Work-Based Project evidence matrix.

Generate documentation to reflect build process during build.

Log hours within EPA documentation (Powerpoint docs - Page 9)

Review final EPA documentation to ensure all processes are being hit and recorded as required. Evidence matrix.

Generate JIRA board to highlight build requirements and milestones. Reference for documentation.

Create build stories.

Create acceptance criteria for project. Must have's, nice to have's. Create additional requirement for Distinction. (Report changes in 2 directions within APP. Back update Portal with assigned information?? Automated project update to save referencing time.)

Create Unit and Inegration tests to suit JIRA requirements.

Add Slack webhook for notifications?
```
Slack Webhook:

    - name: Send Github Slack message
      id: slack
      uses: slackapi/slack-github-action@v1.26.0
      env:
        SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
```





