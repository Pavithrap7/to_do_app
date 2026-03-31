provider "aws" {
  region = "eu-north-1"
}

module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 20.0"

  cluster_name    = "todo-eks"
  cluster_version = "1.29"

  vpc_id = "vpc-07c41864bc5cb5db1"

  subnet_ids = [
    "subnet-0212d84eb91026c21",
    "subnet-029f34d1fc6fa53f1"
  ]

  eks_managed_node_groups = {
    default = {
      desired_size = 1
      max_size     = 2
      min_size     = 1

      instance_types = ["t3.micro"]
    }
  }
}

output "cluster_name" {
  value = module.eks.cluster_name
}
