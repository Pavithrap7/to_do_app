pipeline {
    agent {
        docker { image 'python:3.12' }
    }
    stages {
        stage('Checkout') {
            steps { checkout scm }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip install --upgrade pip'
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Test') {
            steps { sh 'pytest' }
        }
    }
}
