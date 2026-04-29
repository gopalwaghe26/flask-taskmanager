pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Checking out code from GitHub...'
                checkout scm
            }
        }

        stage('Setup Python') {
            steps {
                echo 'Setting up Python virtual environment...'
                sh '''
                    python3 -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running unit tests...'
                sh '''
                    . ${VENV_DIR}/bin/activate
                    pytest test_app.py -v --tb=short
                '''
            }
        }

        stage('Build Success') {
            steps {
                echo 'All tests passed! Ready for Docker build.'
            }
        }
    }

    post {
        success {
            echo 'Pipeline SUCCESS'
        }
        failure {
            echo 'Pipeline FAILED - check test results above.'
        }
    }
}
