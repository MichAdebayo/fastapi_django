variable "resource_group_name" {
  description = "Name of the existing Azure Resource Group"
  type        = string
}

variable "container_registry_name" {
  description = "Name of the existing Azure Container Registry"
  type        = string
}

variable "django_container_name" {
  description = "Name of the Django container"
  type        = string
  default     = "madebayodjango"
}

variable "django_dns_label" {
  description = "DNS label for Django container"
  type        = string
}

variable "django_image" {
  description = "Docker image for Django"
  type        = string
}

variable "cpu" {
  description = "CPU allocation for container"
  type        = number
  default     = 1
}

variable "memory" {
  description = "Memory allocation for container"
  type        = number
  default     = 4
}