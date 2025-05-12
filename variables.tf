variable "docker_image_tag" {
  description = "Docker image tag (e.g., commit SHA)"
  type        = string
}
variable "SERVICE_PRINCIPLE_CLIENT_SECRET" {
  description = "Password for Azure Service Principle Account"
  type        = string
  sensitive   = true
}
variable "FLASK_APP" {
  description = "Path for Flask App"
  type        = string
  sensitive   = true
}
variable "FLASK_DEBUG" {
  description = "State of Flask debug mode"
  type        = string
  sensitive   = true
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
  sensitive   = true
}
variable "WEBSITES_PORT" {
  description = "Website Port"
  type        = string
  sensitive   = true
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
variable "GITHUB_OAUTH_CLIENT_ID" {
  description = "ID for Github OAuth Authentication"
  type        = string
  sensitive   = true
}
variable "GITHUB_OAUTH_CLIENT_SECRET" {
  description = "SECRET for Github OAuth Authentication"
  type        = string
  sensitive   = true
}
variable "TRELLO_API_KEY" {
  description = "SECRET for Trello API Key"
  type        = string
  sensitive   = true
}
variable "TRELLO_API_TOKEN" {
  description = "SECRET for Trello API Token"
  type        = string
  sensitive   = true
}
variable "TRELLO_API_SECRET" {
  description = "SECRET for Trello API Secret"
  type        = string
  sensitive   = true
}
variable "TRELLO_TODO_LIST_ID" {
  description = "SECRET for Trello ToDo List Board ID"
  type        = string
  sensitive   = true
}
variable "LOGS_LEVEL" {
  description = "SECRET for Logs Level"
  type        = string
  sensitive   = true
}
variable "LOGGLY_TOKEN" {
  description = "SECRET for Loggly API Token"
  type        = string
  sensitive   = true
}
variable "LOGGLY_QUERY_TOKEN" {
  description = "SECRET for Loggly Query API Token"
  type        = string
  sensitive   = true
}
variable "MAIL_USERNAME" {
  description = "SECRET for Mail login username"
  type        = string
  sensitive   = true
}
variable "MAIL_PASSWORD" {
  description = "SECRET for Mail login password"
  type        = string
  sensitive   = true
}
variable "MAIL_USE_TLS" {
  description = "SECRET for Mail TLS Status"
  type        = string
  sensitive   = true
}
variable "MAIL_SERVER" {
  description = "SECRET for Mail Server details"
  type        = string
  sensitive   = true
}
variable "MAIL_PORT" {
  description = "SECRET for Mail Server Port Address"
  type        = string
  sensitive   = true
}
variable "MAIL_DEFAULT_SENDED" {
  description = "SECRET for Mail Account default sender address."
  type        = string
  sensitive   = true
}
variable "MAIL_ADMINS" {
  description = "SECRET for Mail Account Admin recipient addresses"
  type        = string
  sensitive   = true
}
variable "SLACK_WEBHOOK_URL" {
  description = "SECRET for Slack URL Webhook"
  type        = string
  sensitive   = true
}