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
  default     = "false"
}
variable "MONGO_CONN_STRING" {
  description = "Mongodb Connection String"
  type        = string
  sensitive   = true
}
variable "MONGODB" {
  description = "Mongodb Name"
  type        = string
  default     = "engportalapidb"
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