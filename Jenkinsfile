pipeline {
    agent any
    tools {
        terraform 'terraform'
    }

    environment {
        FIREBASE_KEY_BASE64 = credentials('firebase_key_id')
        EC2_USER = 'ubuntu'
    }

    options {
        buildDiscarder(logRotator(numToKeepStr: '5'))
        skipDefaultCheckout(true)
    }

    stages {

        stage('Clean Workspace') {
            steps {
                echo 'Deleting old workspace...'
                deleteDir()
            }
        }

        stage('Checkout Master') {
            steps {
                echo 'Cloning master branch...'
                git branch: 'master',
                    url: 'https://github.com/Pavithrap7/to_do_app.git'
            }
        }

        stage('Install Python & Dependencies') {
            steps {
                echo 'Setting up virtual environment for tests...'
                sh '''
                    set -e
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Test Cases') {
            steps {
                echo 'Running pytest...'
                sh '''
                    . venv/bin/activate
                    venv/bin/pytest test/test_main.py -v --maxfail=1 --disable-warnings --junitxml=report.xml
                '''
                junit 'report.xml'
            }
        }

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

                        cd terraform_project
                        terraform init
                        terraform import aws_security_group.todo_sg sg-0758948adf5330ed1 || true
                        terraform apply -auto-approve
                        terraform output
                    '''
                }
            }
        }

        stage('Get EC2 IP') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'jenkin_cred',
                    usernameVariable: 'AWS_ACCESS_KEY_ID',
                    passwordVariable: 'AWS_SECRET_ACCESS_KEY'
                )]) {
                    script {
                        env.EC2_HOST = sh(
                            script: '''
                                export AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
                                export AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
                                cd terraform_project
                                terraform output -raw instance_public_ip
                            ''',
                            returnStdout: true
                        ).trim()
                    }
                }
                echo "EC2 IP is ${EC2_HOST}"
            }
        }

        stage('Install Ansible') {
            steps {
                echo 'Creating virtual environment for Ansible and installing it...'
                sh '''
                    set -e
                    python3 -m venv /opt/ansible-venv
                    . /opt/ansible-venv/bin/activate
                    pip install --upgrade pip
                    pip install ansible
                    ansible --version
                '''
            }
        }

	stage('Deploy using Ansible') {
	    steps {
		echo 'Deploying application via Ansible...'
		sshagent(['ec2_ssh_id']) {
		    sh '''
			# Activate Ansible virtual environment
			. /opt/ansible-venv/bin/activate

			# Prepare dynamic inventory
			mkdir -p ansible
			echo "[web]" > ansible/inventory.ini
			echo "$EC2_HOST ansible_user=ubuntu" >> ansible/inventory.ini

			# Run playbook from the Jenkins workspace
			ansible-playbook -i ansible/inventory.ini ${WORKSPACE}/ansible/deploy.yml \
			    --extra-vars "firebase_key=${FIREBASE_KEY_BASE64}"
		    '''
		}
	    }
	}


	stage('Smoke Tests') {
            steps {
                echo 'Running smoke tests...'
                sh '''
                    . venv/bin/activate
                    pytest test/test_smoke.py --base-url=http://$EC2_HOST:8000 \
                    -v --maxfail=1 --disable-warnings --junitxml=smoke_report.xml
                '''
                junit 'smoke_report.xml'
            }
        }
    }
}
