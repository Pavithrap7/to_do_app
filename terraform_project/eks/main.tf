provider "aws" {
  region = "eu-north-1"
}

terraform {
  backend "s3" {
    bucket = "todo-eks-terraform-state-511197441763"
    key    = "eks/terraform.tfstate"
    region = "eu-north-1"
  }
}

module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 20.0"

  cluster_name    = "todo-eks"
  cluster_version = "1.28"

  vpc_id = "vpc-07c41864bc5cb5db1"

  subnet_ids = [
    "subnet-0212d84eb91026c21",
    "subnet-029f34d1fc6fa53f1"
  ]
create_kms_key = false
cluster_encryption_config = []  # <- make it empty

  eks_managed_node_groups = {
    default = {
      desired_size = 1
      max_size     = 2
      min_size     = 1

      instance_types = ["t3.micro"]
      ami_type = "AL2_x86_64"
    }
  }
}

output "cluster_name" {
  value = module.eks.cluster_name
}
