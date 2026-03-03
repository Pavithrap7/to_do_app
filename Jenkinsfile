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
                echo 'Installing Python and pip...'
                sh '''
                    apt-get update
                    apt-get install -y python3-venv python3-pip
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Test Cases') {
            steps {
                echo 'Running pytest on test/ folder...'
                sh '''
                    venv/bin/pytest test/ -v --maxfail=1 --disable-warnings --junitxml=report.xml --log-cli-level=DEBUG 2>&1 | tee test.log
                '''
                junit 'report.xml'
            }
        }
	stage('Deploy to EC2') {
	    steps {
		sshagent(['ubuntu']) {
		    sh '''
		    ssh -o StrictHostKeyChecking=no ubuntu@13.61.188.43 << 'EOF'
		    set -e

		    # Install dependencies (runs safely even if already installed)
		    sudo apt update -y
		    sudo apt install -y python3 python3-pip python3-venv git

		    mkdir -p ~/app
		    cd ~/app

		    if [ ! -d ".git" ]; then
			git clone https://github.com/Pavithrap7/to_do_app.git .
		    else
			git pull origin master
		    fi

		    if [ ! -d "venv" ]; then
			python3 -m venv venv
		    fi

		    source venv/bin/activate
		    pip install --upgrade pip
		    pip install -r requirements.txt

		    nohup python3 main.py > app.log 2>&1 &
		    EOF
		    '''
		}
	    }
	}

    }
}
