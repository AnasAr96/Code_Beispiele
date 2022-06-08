module myip {
  source  = "4ops/myip/http"
  version = "1.0.0"
}

resource "aws_security_group" "haidi-sg" {
  name        = "haidi-sg"
  description = "Allow inbound traffic"
  vpc_id      = aws_vpc.haidi-vpc.id

  ingress {
    description      = "SSH from VPC"
    from_port        = 22
    to_port          = 22
    protocol         = "tcp"
    cidr_blocks      = ["${module.myip.address}/32"]
  }

  ingress {
    description      = "Backend from VPC"
    from_port        = 3333
    to_port          = 3333
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  tags = {
    Name = "haidi-sg"
  }
}
