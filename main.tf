terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region = "us-east-1"
}

data "aws_vpc" "default" {
  default = true
}

data "aws_subnet_ids" "default" {
  vpc_id            = "${data.aws_vpc.default.id}"
}

resource "aws_security_group" "lb" {
  name        = "lb-sg"
  description = "controls access to the Application Load Balancer (ALB)"

  ingress {
    protocol    = "tcp"
    from_port   = 80
    to_port     = 80
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    protocol    = "-1"
    from_port   = 0
    to_port     = 0
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "ecs_tasks" {
  name        = "ecs-tasks-sg"
  description = "allows inbound access from ALB only"

  ingress {
    protocol        = "tcp"
    from_port       = 4000
    to_port         = 4000
    cidr_blocks     = ["0.0.0.0/0"]
    security_groups = [aws_security_group.lb.id]
  }

  egress {
    protocol    = "-1"
    from_port   = 0
    to_port     = 0
    cidr_blocks = ["0.0.0.0/0"]
  }

}

resource "aws_ecs_task_definition" "deploy_announcements_dev" {

  family                = "deploy_announcements_dev"
  container_definitions = <<DEFINITION
	[
		{
		"name": "ucf-announcements",
		"image": "public.ecr.aws/j2a5t6s3/ucf-announcements:latest",
		"portMappings": [
		  {
		    "containerPort": 8004,
		    "hostPort": 80
		  }
		],
		"memory": 512,
		"cpu": 256
		}
	]	
	DEFINITION
}


resource "aws_ecs_service" "announcements_dev_deployment" {
  name            = "announcements-dev-deployment"
  task_definition = aws_ecs_task_definition.deploy_announcements_dev.arn
  cluster         = aws_ecs_cluster.DevCluster.id
  desired_count   = 1
}

resource "aws_ecs_cluster" "DevCluster" {
  name = "DevCluster"
}
