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


resource "aws_ecs_task_definition" "deploy_announcements_dev" {

  family                = "announcements-deployments"
  container_definitions = <<DEFINITION
	[
		{
		"name": "ucf-announcements",
		"image": "ucf-announcements:latest",
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

