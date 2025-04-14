terraform {
    required_providers {
        azurerm = {
            source = "hashicorp/azurerm"
            version = "~>4.0"
        }
    }
    backend "azurerm" {
        resource_group_name  = "PortalApi"
        storage_account_name = "portalapistorageacc"
        container_name       = "portalapiblob"
        key                  = "terraform.tfstate"
    }
}

provider "azurerm" {
    features {}
    subscription_id = "50ef3721-085f-48dd-a4f1-d17b05980663"
    tenant_id       = "0ae51e19-07c8-4e4b-bb6d-648ee58410f4"
    client_id       = "70bd1492-7521-4c03-bdaf-2f7be682acac"
    client_secret   = var.TF_VAR_SERVICE_PRINCIPLE_CLIENT_SECRET
}
data "azurerm_resource_group" "main" {
    name     = "PortalApi"
}
 
# Azure Container Registry
data "azurerm_container_registry" "acr" {
    name                   = "portalapicontainer"
    resource_group_name    = data.azurerm_resource_group.main.name
}

resource "azurerm_service_plan" "main" {
    name                   = "terraformed-asp"
    location               = data.azurerm_resource_group.main.location
    resource_group_name    = data.azurerm_resource_group.main.name
    os_type                = "Linux"
    sku_name               = "B1"        
}

resource "azurerm_linux_web_app" "main" {
    name                   = "terraformed-engportalapp"
    location               = data.azurerm_resource_group.main.location
    resource_group_name    = data.azurerm_resource_group.main.name
    service_plan_id        = azurerm_service_plan.main.id

    site_config {
        application_stack {
            docker_image_name = "portalapi:latest"
            docker_registry_url = "https://portalapicontainer.azurecr.io"  
            docker_registry_username = var.TF_VAR_DOCKER_SERVER_USR
            docker_registry_password = var.TF_VAR_DOCKER_SERVER_PWD
        }
    }
    app_settings = {
        "FLASK_APP" = var.TF_VAR_FLASK_APP
        "FLASK_DEBUG" = var.TF_VAR_FLASK_DEBUG
        "MONGODBASE_CONN_STRING" = var.TF_VAR_MONGODBASE_CONN_STRING
        "MONGODBASE" = var.TF_VAR_MONGODBASE
        "SECRET_KEY" = var.TF_VAR_SECRET_KEY
        "WEBSITES_PORT" = var.TF_VAR_WEBSITES_PORT
        "WEBSITES_ENABLE_APP_SERVICE_STORAGE" = false
    }
}


resource "azurerm_cosmosdb_account" "main" {
    name                  = "engportalapidbacc"
    location              = data.azurerm_resource_group.main.location
    resource_group_name   = data.azurerm_resource_group.main.name
    offer_type            = "Standard"
    kind                  = "MongoDB"
    mongo_server_version  = "4.2"
        lifecycle { prevent_destroy = true }

    capabilities { 
        name = "EnableMongo"
    }

    capabilities {
        name = "EnableServerless"
    }

    consistency_policy {
        consistency_level = "Strong"
    }

    geo_location {
        location          = "uk south"
        failover_priority = 0
    }

}


data "azurerm_cosmosdb_account" "main" {
  name                = "engportalapidbacc"
  resource_group_name = "PortalApi"
}

resource "azurerm_cosmosdb_mongo_database" "main" {
  name                = "engportalapidbacc"
  resource_group_name = data.azurerm_cosmosdb_account.main.resource_group_name
  account_name        = data.azurerm_cosmosdb_account.main.name
}
