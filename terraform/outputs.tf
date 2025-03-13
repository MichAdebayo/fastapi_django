output "django_url" {
  value = "http://${azurerm_container_group.madebayodjango.ip_address}:8000"
  description = "Public URL of the Django application"
}


