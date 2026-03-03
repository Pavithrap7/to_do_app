pipeline {
    agent any

    environment {
        FIREBASE_KEY_BASE64 = credentials('firebase_key_id')
        EC2_USER = 'ubuntu'
        EC2_HOST = '13.61.188.43'
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
                echo 'Setting up virtual environment...'
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
                    venv/bin/pytest test/ -v --maxfail=1 --disable-warnings --junitxml=report.xml
                '''
                junit 'report.xml'
            }
        }

        stage('Deploy to EC2') {
            steps {
                echo 'Deploying application to EC2...'
                sshagent(['ec2_ssh_id']) {
                    sh '''
                    ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_HOST} << 'EOF'
                    set -e

                    sudo apt update -y
                    sudo apt install -y python3 python3-pip python3-venv git
		    # Remove app folder only if it exists
		    if [ -d "$HOME/application" ]; then
			rm -rf "$HOME/application"
		    else
			mkdir -p "$HOME/application"
		    fi

		    cd "$HOME/application"

                    if [ ! -d ".git" ]; then
                        git clone -b master https://github.com/Pavithrap7/to_do_app.git .
                    else
                        git pull origin master
                    fi

                    if [ ! -d "venv" ]; then
                        python3 -m venv venv
                    fi

                    source venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt

                    pkill -f main.py || true
                    nohup python3 main.py > app.log 2>&1 &
                    EOF
                    '''
                }
            }
        }
    }
}
