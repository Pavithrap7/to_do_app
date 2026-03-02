pipeline {
    agent any
    stages {
        stage('Clean Workspace') {
            steps {
                // Wipes everything in the workspace
                deleteDir()
            }
        }
        stage('Checkout') {
            steps {
                git branch: 'main', 
                    url: 'https://github.com/Pavithrap7/to_do_app.git', 
                    #credentialsId: 'your-cred-id'
            }
        }
        stage('Build') {
            steps {
                echo 'Repo cloned successfully!'
            }
        }
    }
}
