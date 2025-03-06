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
