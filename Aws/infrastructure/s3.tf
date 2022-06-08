resource "aws_s3_bucket" "haidi-ki-s3" {
  bucket = "haidi-ki-s3"
  acl    = "private"
  tags = {
    Name        = "haidi-ki-s3"
    Environment = "Dev"
  }
}

variable "bucketname" {
  type = string
  default = "haidi-frontend-s3"
}
resource "aws_s3_bucket" "haidi-frontend-s3" {
  bucket = var.bucketname
  acl    = "public-read"
  force_destroy = true

  # Abhängigkeit weil das Frontend erst die IP von der EC2 Instanz (eip) braucht
  depends_on = [aws_eip.haidi-backend-eip]

  policy = jsonencode(
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Sid": "PublicReadGetObject",
          "Effect": "Allow",
          "Principal": "*",
          "Action": [
            "s3:GetObject"
          ],
          "Resource": [
            "arn:aws:s3:::${var.bucketname}/*"
          ]
        }
      ]
    }
  )

  tags = {
    Name        = "haidi-frontend-s3"
    Environment = "Dev"
  }

  website {
    index_document = "index.html"
    error_document = "error.html"
  }

  # Change IP in frontend
  provisioner "local-exec" {
    command = "./update-angular-ip.sh ${aws_eip.haidi-backend-eip.public_ip}"
  }

  # Build Angular Webapp
  provisioner "local-exec" {
    command = "./build-angular.sh"
  }

  # Upload website
  provisioner "local-exec" {
    command = "aws s3 sync ../../haidi-frontend/dist/haidi-frontend/ s3://haidi-frontend-s3"
  }
}
