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

        stage('Build / Test') {
            steps {
                echo 'Repo cloned successfully on master branch!'
                // Add your build/test commands here
            }
        }
    }
}
