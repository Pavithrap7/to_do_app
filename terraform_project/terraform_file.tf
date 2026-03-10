provider "aws" {
  region = "eu-north-1"
}

# Security Group
resource "aws_security_group" "todo_sg" {
  name        = "todo_app_sg"
  description = "Allow SSH, HTTP, HTTPS and App"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# EC2 Instance
resource "aws_instance" "todo_server" {

  ami           = "ami-0989fb15ce71ba39e"   # Ubuntu 22.04
  instance_type = "t3.micro"

  # Existing AWS key pair name
  key_name = "todo_server"

  vpc_security_group_ids = [
    aws_security_group.todo_sg.id
  ]

  tags = {
    Name = "Terraform-Todo-Server"
  }
}

# Output EC2 public IP
output "instance_public_ip" {
  value = aws_instance.todo_server.public_ip
}
