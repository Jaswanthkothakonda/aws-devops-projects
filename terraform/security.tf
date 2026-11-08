# Security group for the public Application Load Balancer
resource "aws_security_group" "alb" {
  name        = "${var.project_name}-${var.environment}-alb-sg"
  description = "Allow HTTP from CloudFront origin-facing servers only"
  vpc_id      = data.aws_vpc.existing.id

  ingress {
    description     = "Allow HTTP traffic from CloudFront origin-facing servers"
    from_port       = 80
    to_port         = 80
    protocol        = "tcp"
    prefix_list_ids = ["pl-0a25c3463226fcc61"]
  }

  egress {
    description = "Allow application traffic to the BeastEats VPC"
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = [data.aws_vpc.existing.cidr_block]
  }

  tags = {
    Name        = "${var.project_name}-${var.environment}-alb-sg"
    Project     = "BeastEats"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

# Security group for the private application interface
resource "aws_security_group" "app" {
  name        = "${var.project_name}-${var.environment}-app-sg"
  description = "Allow application traffic only from BeastEats ALB"
  vpc_id      = data.aws_vpc.existing.id

  ingress {
    description     = "Allow Gunicorn traffic from ALB only"
    from_port       = 8000
    to_port         = 8000
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
  }

  egress {
    description = "Allow outbound connectivity for ECR and SSM"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "${var.project_name}-${var.environment}-app-sg"
    Project     = "BeastEats"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}
