pipeline {
    agent any

    tools {
        terraform 'terraform'
        // You can also specify kubectl or aws CLI if installed on the agent
    }

    environment {
        FIREBASE_KEY_BASE64 = credentials('firebase_key_id')
        AWS_REGION = 'us-east-1'
        ECR_REPO = '123456789012.dkr.ecr.us-east-1.amazonaws.com/todo-app'
    }

    options {
        buildDiscarder(logRotator(numToKeepStr: '5'))
        skipDefaultCheckout(true)
    }

    stages {

        // -------------------------------
        stage('Clean Workspace') {
            steps {
                echo 'Deleting old workspace...'
                deleteDir()
            }
        }

        // -------------------------------
        stage('Checkout Code') {
            steps {
                echo 'Cloning repository...'
                git branch: 'master',
                    url: 'https://github.com/Pavithrap7/to_do_app.git'
            }
        }

        // -------------------------------
        stage('Install Python & Dependencies') {
	    agent {
		docker { image 'python:3.13-slim' }
	    }
            steps {
                echo 'Setting up virtual environment...'
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        // -------------------------------
        stage('Run Unit Tests') {
            steps {
                echo 'Running pytest...'
                sh '''
                    . venv/bin/activate
                    pytest test/test_main.py -v --maxfail=1 --disable-warnings --junitxml=report.xml
                '''
                junit 'report.xml'
            }
        }

        // -------------------------------
        stage('Build Docker Image') {
	    agent {
		docker { image 'docker:24.0.5-cli' }
	    }
            steps {
                echo 'Building Docker image...'
                sh '''
                    docker build -t todo-app:${BUILD_NUMBER} .
                    aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REPO
                    docker tag todo-app:${BUILD_NUMBER} $ECR_REPO:${BUILD_NUMBER}
                    docker push $ECR_REPO:${BUILD_NUMBER}
                '''
            }
        }

        // -------------------------------
        stage('Terraform Apply') {
            steps {
                echo 'Creating infrastructure with Terraform...'
                withCredentials([usernamePassword(
                    credentialsId: 'jenkin_cred',
                    usernameVariable: 'AWS_ACCESS_KEY_ID',
                    passwordVariable: 'AWS_SECRET_ACCESS_KEY'
                )]) {
                    sh '''
                        export AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
                        export AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
                        export AWS_REGION=$AWS_REGION

                        cd terraform_project
                        terraform init
                        terraform apply -auto-approve
                        terraform output -raw eks_cluster_name
                    '''
                }
            }
        }

        // -------------------------------
        stage('Ansible Node Setup (Optional)') {
            steps {
                echo 'Running Ansible to configure nodes...'
                sh '''
                    ansible-playbook ansible/install_docker.yml -i ansible/inventory.ini
                '''
            }
        }

        // -------------------------------
        stage('Kubernetes Deploy') {
            steps {
                echo 'Deploying to Kubernetes...'
                sh '''
                    aws eks update-kubeconfig --name $(cd terraform_project && terraform output -raw eks_cluster_name) --region $AWS_REGION

                    kubectl apply -f k8s/deployment.yaml
                    kubectl apply -f k8s/service.yaml
                '''
            }
        }

        // -------------------------------
        stage('Smoke Tests') {
            steps {
                echo 'Running smoke tests...'
                sh '''
                    . venv/bin/activate
                    pytest test/test_smoke.py --base-url=http://$(kubectl get svc todo-service -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'):80 -v --maxfail=1 --disable-warnings --junitxml=smoke_report.xml
                '''
                junit 'smoke_report.xml'
            }
        }
    }
} 
