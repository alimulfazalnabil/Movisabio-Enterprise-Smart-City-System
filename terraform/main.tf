terraform {
  required_version = ">= 1.6.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.85.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.6.0"
    }
  }
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "rg-${var.project_name}-${var.environment}"
  location = var.location
}

resource "azurerm_kubernetes_cluster" "aks" {
  name                = "aks-${var.project_name}-${var.environment}"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  dns_prefix          = "${var.project_name}-aks"

  default_node_pool {
    name       = "defaultpool"
    node_count = 3
    vm_size    = "Standard_D4s_v5"
    os_disk_size_gb = 128
  }

  identity {
    type = "SystemAssigned"
  }

  tags = {
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

resource "azurerm_postgresql_flexible_server" "postgres" {
  name                   = "psql-${var.project_name}-${var.environment}"
  resource_group_name    = azurerm_resource_group.rg.name
  location               = azurerm_resource_group.rg.location
  version                = "16"
  administrator_login    = "movisabioadmin"
  administrator_password = "Password12345!"
  storage_mb             = 32768
  sku_name               = "B_Standard_B1ms"
}

resource "azurerm_redis_cache" "redis" {
  name                = "redis-${var.project_name}-${var.environment}"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  capacity            = 1
  family              = "C"
  sku_name            = "Basic"
  enable_non_ssl_port = false
  minimum_tls_version = "1.2"
}

resource "azurerm_iothub" "iothub" {
  name                = "iothub-${var.project_name}-${var.environment}"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  sku {
    name     = "S1"
    capacity = 1
  }
}
