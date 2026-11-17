resource "aws_instance" "beasteats" {
  ami                         = "ami-0f87c4386dc5a47e7"
  instance_type               = var.instance_type
  subnet_id                   = var.subnet_id
  vpc_security_group_ids      = [aws_security_group.app.id]
  associate_public_ip_address = true
  iam_instance_profile        = var.instance_profile_name

  user_data = <<USERDATA
#!/bin/bash
set -eux

dnf install -y docker xfsprogs

usermod -aG docker ec2-user
mkdir -p /app/instance

cat > /usr/local/sbin/mount-beasteats-data.sh <<'SCRIPT'
#!/bin/bash
set -e

DEVICE="/dev/disk/by-id/nvme-Amazon_Elastic_Block_Store_${replace(aws_ebs_volume.app_data.id, "-", "")}"

for attempt in $(seq 1 60); do
    if [ -b "$DEVICE" ]; then
        break
    fi
    sleep 10
done

if [ ! -b "$DEVICE" ]; then
    echo "BeastEats EBS data volume not detected: $DEVICE"
    exit 1
fi

if ! blkid "$DEVICE" >/dev/null 2>&1; then
    mkfs.xfs "$DEVICE"
fi

FILESYSTEM_TYPE=$(blkid -s TYPE -o value "$DEVICE")

if [ "$FILESYSTEM_TYPE" != "xfs" ]; then
    echo "Unexpected filesystem type: $FILESYSTEM_TYPE"
    exit 1
fi

UUID=$(blkid -s UUID -o value "$DEVICE")

if ! grep -q "$UUID" /etc/fstab; then
    echo "UUID=$UUID /app/instance xfs defaults,nofail 0 2" >> /etc/fstab
fi

if ! mountpoint -q /app/instance; then
    mount /app/instance
fi
SCRIPT

chmod 750 /usr/local/sbin/mount-beasteats-data.sh

cat > /etc/systemd/system/beasteats-data-mount.service <<'UNIT'
[Unit]
Description=Mount BeastEats persistent EBS data volume
After=local-fs.target
Before=docker.service

[Service]
Type=oneshot
ExecStart=/usr/local/sbin/mount-beasteats-data.sh
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
UNIT

systemctl daemon-reload
systemctl enable --now beasteats-data-mount.service
systemctl enable --now docker
USERDATA

  root_block_device {
    volume_type           = "gp3"
    volume_size           = 8
    encrypted             = true
    delete_on_termination = true
  }

  tags = {
    Name        = "${var.project_name}-${var.environment}-app"
    Project     = var.project_name
    Environment = var.environment
  }

  lifecycle {
    ignore_changes = [user_data]
  }
}
