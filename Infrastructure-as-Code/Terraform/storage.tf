resource "aws_ebs_volume" "app_data" {
  availability_zone = data.aws_subnet.public_a.availability_zone
  size              = 5
  type              = "gp3"
  encrypted         = true

  tags = {
    Name        = "${var.project_name}-${var.environment}-app-data"
    Project     = var.project_name
    Environment = var.environment
  }
}

resource "aws_volume_attachment" "app_data" {
  device_name = "/dev/sdf"
  volume_id   = aws_ebs_volume.app_data.id
  instance_id = aws_instance.beasteats.id
}
