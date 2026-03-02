pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                // Pulls the code from your specific repo
                git url: 'https://github.com/Pavithrap7/to_do_app.git', 
                    branch: 'master'
            }
        }

        stage('Install Dependencies') {
            steps {
                // Adjust based on your app (e.g., npm install for JS or pip for Python)
                echo 'Installing dependencies...'
                sh 'npm install' 
            }
        }

        stage('Test') {
            steps {
                echo 'Running tests...'
                sh 'npm test'
            }
        }

        stage('Build') {
            steps {
                echo 'Building application...'
                sh 'npm run build'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying to staging server...'
                // Add your deployment commands here
            }
        }
    }

}
