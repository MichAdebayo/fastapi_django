# Get existing resource group
data "azurerm_resource_group" "existing_rg" {
  name = var.resource_group_name
}
# Get existing container registry
data "azurerm_container_registry" "existing_acr" {
  name                = var.container_registry_name
  resource_group_name = data.azurerm_resource_group.existing_rg.name
}

# Deploy Django container
resource "azurerm_container_group" "madebayodjango" {
  name                = var.django_container_name
  location            = data.azurerm_resource_group.existing_rg.location
  resource_group_name = data.azurerm_resource_group.existing_rg.name
  os_type             = "Linux"
  dns_name_label      = var.django_dns_label

  container {
    name   = "madebayodjango"
    image  = var.django_image
    cpu    = var.cpu
    memory = var.memory

    ports {
      port     = 8000
      protocol = "TCP"
    }

    environment_variables = {
      ENVIRONMENT = "production"
    }
  }

  image_registry_credential {
    server   = data.azurerm_container_registry.existing_acr.login_server 
    username = data.azurerm_container_registry.existing_acr.admin_username
    password = data.azurerm_container_registry.existing_acr.admin_password
  }
}

