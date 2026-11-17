resource "aws_cloudfront_distribution" "beasteats" {
  enabled         = true
  comment         = "BeastEats public HTTPS distribution"
  price_class     = "PriceClass_100"
  is_ipv6_enabled = true

  origin {
    domain_name = aws_lb.beasteats.dns_name
    origin_id   = "beasteats-alb-origin"

    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "http-only"
      origin_ssl_protocols   = ["TLSv1.2"]
    }

    custom_header {
      name  = "X-Origin-Verify"
      value = var.origin_verify_header_value
    }
  }

  default_cache_behavior {
    target_origin_id       = "beasteats-alb-origin"
    viewer_protocol_policy = "redirect-to-https"

    allowed_methods = [
      "DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"
    ]

    cached_methods = ["GET", "HEAD", "OPTIONS"]

    cache_policy_id = "4135ea2d-6df8-44a3-9df3-4b5a84be39ad"

    origin_request_policy_id = "b689b0a8-53d0-40ab-baf2-68738e2966ac"

    compress = true
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = true
    minimum_protocol_version       = "TLSv1.2_2021"
  }

  tags = {
    Name        = "${var.project_name}-${var.environment}-cloudfront"
    Project     = "BeastEats"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}
