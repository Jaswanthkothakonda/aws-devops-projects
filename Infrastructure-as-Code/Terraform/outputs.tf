output "vpc_id" {
  description = "Existing BeastEats VPC ID"
  value       = data.aws_vpc.existing.id
}

output "public_subnet_a" {
  description = "Existing public subnet in ap-south-2a"
  value       = data.aws_subnet.public_a.id
}

output "public_subnet_b" {
  description = "Existing public subnet in ap-south-2b"
  value       = data.aws_subnet.public_b.id
}

output "private_subnet_a" {
  description = "Existing private subnet in ap-south-2a"
  value       = data.aws_subnet.private_a.id
}

output "ecr_repository_url" {
  description = "Existing BeastEats ECR repository URL"
  value       = data.aws_ecr_repository.beasteats.repository_url
}

output "cloudfront_domain_name" {
  description = "Public HTTPS URL for BeastEats"
  value       = aws_cloudfront_distribution.beasteats.domain_name
}

output "cloudfront_url" {
  description = "Public HTTPS endpoint"
  value       = "https://${aws_cloudfront_distribution.beasteats.domain_name}"
}

output "alb_dns_name" {
  description = "Application Load Balancer DNS name"
  value       = aws_lb.beasteats.dns_name
}
