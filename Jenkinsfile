pipeline {
    agent any

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
		    . bin/venv/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

    }
}
