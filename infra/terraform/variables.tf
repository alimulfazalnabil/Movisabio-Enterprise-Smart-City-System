variable "environment" {
  description = "Deployment environment (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "aws_region" {
  description = "AWS Region"
  type        = string
  default     = "us-east-1"
}

variable "db_username" {
  description = "PostgreSQL Admin Username"
  type        = string
  sensitive   = true
}

variable "db_password" {
  description = "PostgreSQL Admin Password"
  type        = string
  sensitive   = true
}
