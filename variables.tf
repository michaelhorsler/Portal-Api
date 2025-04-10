variable "SERVICE_PRINCIPLE_CLIENT_SECRET" {
  description = "Password for Azure Service Principle Account"
  type        = string
  sensitive   = true
}
variable "FLASK_APP" {
  description = "Path for Flask App"
  type        = string
  default     = "portalapi/app"
}
variable "FLASK_DEBUG" {
  description = "State of Flask debug mode"
  type        = string
  default     = "true"
}
variable "MONGODBASE_CONN_STRING" {
  description = "Mongodb Connection String"
  type        = string
  sensitive   = true
}
variable "MONGODBASE" {
  description = "Mongodb Name"
  type        = string
  sensitive   = true
}
variable "SECRET_KEY" {
  description = "Cookie Variable"
  type        = string
  default     = "secret-key"
}
variable "WEBSITES_PORT" {
  description = "Website Port"
  type        = string
  default     = "5000"
}
variable "DOCKER_SERVER_USR" {
  description = "Username for Azure Container Registry"
  type        = string
  sensitive   = true
}
variable "DOCKER_SERVER_PWD" {
  description = "Password for Azure Container Registry"
  type        = string
  sensitive   = true
}
variable "container_registry_name" {
  type        = string
  description = "Azure Container Registry Name"
  default     = "portalapicontainer"
}