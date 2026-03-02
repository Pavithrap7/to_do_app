pipeline {
    agent any
    environment {
        // Inject Firebase key from Jenkins credentials
        FIREBASE_KEY_BASE64 = credentials('firebase_key_id')
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
		    venv/bin/pytest test/ -v --maxfail=1 --disable-warnings --junitxml=report.xml 2>&1 | tee test.log --log-cli-level=DEBUG
		'''
		junit 'report.xml'
	    }
	}

    }
}
