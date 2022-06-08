resource "aws_iam_role" "haidi-iam-role" {
  name               = "haidi-iam-role"
  assume_role_policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
      {
        "Sid": "",
        "Effect": "Allow",
        "Principal": {
          "Service": "ec2.amazonaws.com"
        },
        "Action": "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "haidi-iam-role-s3-attachement" {
  role       = aws_iam_role.haidi-iam-role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

resource "aws_iam_role_policy_attachment" "haidi-iam-role-lambda-attachement" {
  role       = aws_iam_role.haidi-iam-role.name
  policy_arn = "arn:aws:iam::aws:policy/AWSLambda_FullAccess"
}

resource "aws_iam_instance_profile" "haidi-instance-profile" {
  name = "haidi-instance-profile"
  role = aws_iam_role.haidi-iam-role.name
}
