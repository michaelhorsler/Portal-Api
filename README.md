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
