# Portal-Api
DevOps Cohort - EPA Assessment Project


## Reference Paths and setup.

### Setup process for new Project.

Github repository:  https://github.com/michaelhorsler/Portal-Api.git

Github Actions CI Pipeline: https://github.com/michaelhorsler/Portal-Api/actions/workflows/portal-api-ci-pipeline.yml

Docker Hub: https://hub.docker.com/repositories/michaelsminis

Azure Portal:  https://portal.azure.com/#home 

Login: (username)@bosch.com

Applied for Azure 60 day Sandbox license for project.
Prove if operation is suffiient or upgrade to Development license.

Portal-Api Resource Group: TBA. Request to be submitted.

## Setup new project.
Create new repository within Github. i.e. Portal-Api.Git.

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