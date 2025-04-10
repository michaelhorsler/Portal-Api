terraform {
    required_providers {
        azurerm = {
            source = "hashicorp/azurerm"
            version = "~>4.0"
        }
    }
}

provider "azurerm" {
    features {}
    subscription_id = "50ef3721-085f-48dd-a4f1-d17b05980663"
    tenant_id       = "0ae51e19-07c8-4e4b-bb6d-648ee58410f4"
    client_id       = "70bd1492-7521-4c03-bdaf-2f7be682acac"
    client_secret   = var.SERVICE_PRINCIPLE_CLIENT_SECRET
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
            docker_registry_username = var.DOCKER_SERVER_USR
            docker_registry_password = var.DOCKER_SERVER_PWD
        }
    }
    app_settings = {
        "FLASK_APP" = var.FLASK_APP
        "FLASK_DEBUG" = var.FLASK_DEBUG
        "MONGODBASE_CONN_STRING" = var.MONGODBASE_CONN_STRING
        "MONGODBASE" = var.MONGODBASE
        "SECRET_KEY" = var.SECRET_KEY
        "WEBSITES_PORT" = var.WEBSITES_PORT
        WEBSITES_ENABLE_APP_SERVICE_STORAGE = false
    }
}