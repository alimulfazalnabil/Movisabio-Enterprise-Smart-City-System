terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# --- Core Networking ---
module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
  name   = "movisabio-${var.environment}-vpc"
  cidr   = "10.0.0.0/16"
  
  azs             = ["us-east-1a", "us-east-1b"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24"]
  
  enable_nat_gateway = true
}

# --- PostGIS Database (Territorial Data Layer) ---
resource "aws_db_instance" "postgis" {
  identifier           = "movisabio-postgis-${var.environment}"
  engine               = "postgres"
  engine_version       = "15.3"
  instance_class       = "db.t3.medium"
  allocated_storage    = 100
  
  db_name              = "movisabio_territory"
  username             = var.db_username
  password             = var.db_password
  
  vpc_security_group_ids = [aws_security_group.db_sg.id]
  db_subnet_group_name   = module.vpc.database_subnet_group
  
  skip_final_snapshot = var.environment == "dev" ? true : false
}

# --- Event Bus (MSK / Kafka) ---
resource "aws_msk_cluster" "event_bus" {
  cluster_name           = "movisabio-events-${var.environment}"
  kafka_version          = "3.4.0"
  number_of_broker_nodes = 3
  
  broker_node_group_info {
    instance_type = "kafka.t3.small"
    client_subnets = module.vpc.private_subnets
    security_groups = [aws_security_group.kafka_sg.id]
  }
}
