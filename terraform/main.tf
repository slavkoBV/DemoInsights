terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "5.41.0"
    }
  }
}

provider "aws" {
  region = var.Region
}

resource "aws_ecr_repository" "repo" {
  name = "demo-insights"
}

resource "aws_s3_bucket" "bucket" {
  bucket = var.BucketName
}

resource "aws_cloudwatch_log_group" "lg" {
  name = "demo-insights-lg"
}

resource "aws_ecs_cluster" "cluster" {
  name = "demo-insights-cluster"
}

resource "aws_iam_policy" "task_policy" {
  name = "TaskAccessPolicy"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action   = ["transcribe:StartTranscriptionJob",
          "transcribe:GetTranscriptionJob", "s3:GetObject", "s3:PutObject"]
        Effect   = "Allow"
        Resource = "*"
      },
    ]
  })
}

resource "aws_iam_role" "task_role" {
  name = "task_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action    = "sts:AssumeRole"
        Effect    = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      }]
  })
  managed_policy_arns = [aws_iam_policy.task_policy.arn]
}

resource "aws_iam_role" "task_execution_role" {
  name = "task_execution_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action    = "sts:AssumeRole"
        Effect    = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      }]
  })
  managed_policy_arns = ["arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"]
}

resource "aws_default_vpc" "default" {
  tags = {
    Name = "Default VPC"
  }
}

resource "aws_security_group" "container_sg" {
  name = "container_sg"
  vpc_id = aws_default_vpc.default.id
  ingress {
    from_port = 8000
    to_port = 8000
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
      from_port        = 0
      to_port          = 0
      protocol         = "-1"
      cidr_blocks      = ["0.0.0.0/0"]
      ipv6_cidr_blocks = ["::/0"]
    }
}

resource "aws_ecs_task_definition" "insights-task" {
  family = "task"
  container_definitions = jsonencode([{
    name = "insights-container"
    image = var.AppImage
    portMappings = [
      {
        containerPort = 8000
        hostPort = 8000
      }
    ]
    environment = [
      {
        "name": "TRANSCRIPTION_BUCKET", "value": var.BucketName
      }
    ]
    logConfiguration = {
      logDriver = "awslogs",
      options = {
        "awslogs-group": aws_cloudwatch_log_group.lg.id,
        "awslogs-region": var.Region,
        "awslogs-stream-prefix": "ecs"
      }
    }
  }])
  task_role_arn = aws_iam_role.task_role.arn
  execution_role_arn = aws_iam_role.task_execution_role.arn
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 256
  memory                   = 512
}

resource "aws_default_subnet" "default_subnet" {
  availability_zone = var.SubnetRegion
}

resource "aws_ecs_service" "insights_service" {
  name = "insights-service"
  cluster = aws_ecs_cluster.cluster.id
  task_definition = aws_ecs_task_definition.insights-task.arn
  desired_count = 1
  launch_type = "FARGATE"
  network_configuration {
    subnets = [aws_default_subnet.default_subnet.id]
    assign_public_ip = true
    security_groups = [aws_security_group.container_sg.id]
  }
}