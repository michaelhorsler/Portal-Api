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
            docker_image_name = "portalapi:${var.docker_image_tag}"
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
        "WEBSITES_ENABLE_APP_SERVICE_STORAGE" = false
        "GITHUB_OAUTH_CLIENT_ID" = var.GITHUB_OAUTH_CLIENT_ID
        "GITHUB_OAUTH_CLIENT_SECRET" = var.GITHUB_OAUTH_CLIENT_SECRET
        "TRELLO_API_KEY" = var.TRELLO_API_KEY
        "TRELLO_API_SECRET" = var.TRELLO_API_SECRET
        "TRELLO_API_TOKEN" = var.TRELLO_API_TOKEN
        "TRELLO_TODO_LIST_ID" = var.TRELLO_TODO_LIST_ID
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


resource "azurerm_kubernetes_cluster" "main" {
  name                = "portalapiAKSCluster"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  dns_prefix          = "portalapiA-PortalApi-50ef37"

  default_node_pool {
    name       = "nodepool1"
    node_count = 1
    vm_size    = "standard_l8s_v3"
    auto_scaling_enabled = "true"
    max_count  = 5
    min_count  = 1
  }

  identity {
    type = "SystemAssigned"
  }

  lifecycle {
    ignore_changes = [
      linux_profile,
    ]
  }

  tags = {
    Environment = "Production"
  }
}

