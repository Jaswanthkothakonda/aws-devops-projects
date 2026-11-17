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
  description = "Existing public subnet for the BeastEats EC2 deployment"
  type        = string
  default     = "subnet-0fa5650ba25138dd1"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro"
}

variable "instance_profile_name" {
  description = "IAM instance profile for SSM and ECR access"
  type        = string
  default     = "BeastEats-App-EC2-Role"
}


variable "origin_verify_header_value" {
  description = "Private header value used to verify CloudFront origin requests"
  type        = string
  sensitive   = true
}
