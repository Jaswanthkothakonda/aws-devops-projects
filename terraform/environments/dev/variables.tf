variable "project_name" {
  description = "Name of the application project"
  type        = string
  default     = "beasteats"
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "dev"
}

variable "aws_region" {
  description = "AWS deployment region"
  type        = string
  default     = "ap-south-2"
}

variable "vpc_id" {
  description = "Existing BeastEats VPC ID"
  type        = string
  default     = "vpc-0ffab745b1d5f80e2"
}

variable "subnet_id" {
  description = "Existing subnet for the EC2 deployment"
  type        = string
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro"
}
