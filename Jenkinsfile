pipeline {
    agent any

    options {
        // Always clean the workspace before starting
        wipeWorkspace()
        // Keep logs from previous builds
        ansiColor('xterm')
        timestamps()
    }

    stages {

        stage('Checkout') {
            steps {
                echo "Cloning repository..."
                checkout scm
            }
        }

        stage('Run Python Tests') {
            agent {
                docker {
                    // Use official Python image
                    image 'python:3.12'
                    // Mount the Jenkins workspace inside the container
                    args '-v $WORKSPACE:$WORKSPACE -w $WORKSPACE'
                }
            }
            steps {
                echo "Upgrading pip and installing dependencies..."
                sh 'pip install --upgrade pip'
                sh 'pip install -r requirements.txt'

                echo "Running pytest..."
                sh 'pytest --maxfail=1 --disable-warnings -q'
            }
        }
    }

    post {
        always {
            echo "Cleaning up workspace..."
            cleanWs()
        }
        success {
            echo "Build and tests completed successfully ✅"
        }
        failure {
            echo "Build or tests failed ❌"
        }
    }
}
