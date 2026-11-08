# Existing BeastEats VPC
data "aws_vpc" "existing" {
  id = var.vpc_id
}

# Public subnet in Availability Zone 2a
data "aws_subnet" "public_a" {
  id = "subnet-0fa5650ba25138dd1"
}

# Public subnet in Availability Zone 2b
data "aws_subnet" "public_b" {
  id = "subnet-0522549c4aa32fd28"
}

# Private application subnet in Availability Zone 2a
data "aws_subnet" "private_a" {
  id = "subnet-0798524c0e5b03fd9"
}

# Existing BeastEats ECR repository
data "aws_ecr_repository" "beasteats" {
  name = "beasteats"
}
