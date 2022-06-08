resource "aws_vpc" "haidi-vpc" {
  cidr_block       = "10.0.0.0/24"
  instance_tenancy = "default"

  tags = {
    Name = "haidi-vpc"
  }
}

resource "aws_subnet" "haidi-sn-dmz" {
  vpc_id     = aws_vpc.haidi-vpc.id
  cidr_block = "10.0.0.0/24"

  tags = {
    Name = "haidi-sn-dmz"
  }
}

resource "aws_internet_gateway" "haidi-igw" {
  vpc_id = aws_vpc.haidi-vpc.id

  tags = {
    Name = "haidi-igw"
  }
}

resource "aws_route_table" "haidi-rt" {
  vpc_id = aws_vpc.haidi-vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.haidi-igw.id
  }

  tags = {
    Name = "haidi-rt"
  }
}

resource "aws_route_table_association" "haidi-rt-association" {
  subnet_id      = aws_subnet.haidi-sn-dmz.id
  route_table_id = aws_route_table.haidi-rt.id
}
