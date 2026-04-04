provider "aws" {
  region = "us-east-1" # Change to your desired region
}

resource "aws_s3_bucket" "frontend_bucket" {
  bucket = "your-s3-bucket-name" # Replace with your bucket name
  acl    = "public-read"

  website {
    index_document = "index.html"
    error_document = "index.html"
  }
}

resource "aws_ecs_cluster" "backend_cluster" {
  name = "backend-cluster"
}

resource "aws_ecs_task_definition" "backend_task" {
  family                   = "backend-task"
  container_definitions    = jsonencode([
    {
      name      = "backend-container",
      image     = "your-backend-image", # Replace with your Docker image
      cpu       = 256,
      memory    = 512,
      essential = true,
      portMappings = [
        {
          containerPort = 5000,
          hostPort      = 5000,
        },
      ],
    },
  ])
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = "256"
  memory                   = "512"
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
}

resource "aws_iam_role" "ecs_task_execution_role" {
  name = "ecsTaskExecutionRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      },
    ]
  })

  managed_policy_arns = [
    "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy",
  ]
}

resource "aws_ecs_service" "backend_service" {
  name            = "backend-service"
  cluster         = aws_ecs_cluster.backend_cluster.id
  task_definition = aws_ecs_task_definition.backend_task.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets         = ["subnet-12345678"] # Replace with your subnet IDs
    security_groups = ["sg-12345678"]    # Replace with your security group IDs
    assign_public_ip = true
  }
}