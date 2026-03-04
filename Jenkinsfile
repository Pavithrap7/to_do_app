pipeline {
    agent any

    environment {
        EC2_USER = 'ubuntu'
        EC2_HOST = '13.53.131.13'
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
                echo 'Setting up local virtual environment...'
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
                // Ensure FIREBASE_KEY_BASE64 is available for Python
                withEnv(["FIREBASE_KEY_BASE64=${FIREBASE_KEY_BASE64}"]) {
                    sh '''
                        venv/bin/pytest test/ -v --maxfail=1 --disable-warnings --junitxml=report.xml
                    '''
                }
                junit 'report.xml'
            }
        }

        stage('Deploy to EC2') {
            steps {
                echo 'Deploying application to EC2...'
                sshagent(['ec2_ssh_id']) {
                    // Use credentials safely on remote server
                    withCredentials([string(credentialsId: 'firebase_key_id', variable: 'FIREBASE_KEY_BASE64')]) {
                        sh """
                        ssh -tt -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_HOST} << 'EOF'
                        set -e

                        # Install system packages (if needed)
                        sudo apt update -y
                        sudo apt install -y python3 python3-pip python3-venv git

                        # Set working directory
                        APP_DIR="/home/ubuntu/application"
                        mkdir -p "\$APP_DIR"
                        cd "\$APP_DIR"

                        # Clone or update repo
                        if [ ! -d ".git" ]; then
                            git clone -b master https://github.com/Pavithrap7/to_do_app.git .
                        else
                            git fetch origin
                            git reset --hard origin/master
                        fi

                        # Setup virtual environment
                        if [ ! -d "venv" ]; then
                            python3 -m venv venv
                        fi
                        source venv/bin/activate

                        # Firebase key
                        echo "$FIREBASE_KEY_BASE64" | base64 --decode > firebase_key.json
                        chmod 600 firebase_key.json

                        # Install Python dependencies
                        venv/bin/pip install --upgrade pip
                        venv/bin/pip install -r requirements.txt

                        # Restart FastAPI app
                        pkill -f main.py || true
                        nohup venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 > app.log 2>&1 &
EOF
                        """
                    }
                }
            }
        }
    }
}
