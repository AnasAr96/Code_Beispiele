
resource "aws_key_pair" "deployer" {
  key_name   = "haidi-key-par-backend"
  public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCKs5Sm2KTXh2X+0Fancz9qPBcre+iGJvHpnmD1D8aHCSjj/9cLv/zn7dTuSFW61a9cCLgwhZFv09Ngyry9Imm9Yx+55XFO95sdlUPMY6AofnRMad/HmjxOS6XpZdPEv0pAEdy1o1FRFF1Z0vj5Jb4NVvOnQJah4ECnoxaG5qUnCahkOLRZjef9K6SuTK2CbXtT99EKfB7GsgDAoz/qTV9EY4Ycey9XrlTPnqIcrZZSbvhByxFUGGdGh0phUVGPLBEMI/CkYky0gBAp4/n0K2R8g5MIGgyduMUHhjL2Or4i/qWeK0G/TqSnM2RbC4b0Hd0LeqI3piEnFX6ewRSTe/CF"

  tags = {
    Name = "haidi-key-pair"
  }
}

data "aws_ami" "haidi-linux-ami" {
  most_recent = true

  filter {
    name   = "name"
    values = ["haidi-linux-aws"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["214138175513"]
}

output "haidi_backend_ami_id" {
  value = data.aws_ami.haidi-linux-ami.id
}

output "haidi_backend_ami_name" {
  value = data.aws_ami.haidi-linux-ami.name
}

resource "aws_instance" "haidi-backend-instance" {
  ami           = data.aws_ami.haidi-linux-ami.id
  instance_type = "t2.micro"
  key_name = aws_key_pair.deployer.key_name
  security_groups = [aws_security_group.haidi-sg.id]
  subnet_id = aws_subnet.haidi-sn-dmz.id
  iam_instance_profile = aws_iam_instance_profile.haidi-instance-profile.id

  tags = {
    Name = "haidi-backend-instance"
  }
}

resource "aws_eip" "haidi-backend-eip" {
  instance = aws_instance.haidi-backend-instance.id
  vpc      = true
}

output "haidi_backend_public-ip" {
  value = aws_eip.haidi-backend-eip.public_ip
}
