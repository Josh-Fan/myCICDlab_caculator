pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
    }

    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/Josh-Fan/myCICDlab_caculator.git', branch: 'main'
            }
        }

        stage('Setup Python Env') {
            steps {
                sh 'python3 -m venv $VENV_DIR'
                sh './$VENV_DIR/bin/pip install -r requirements.txt'
            }
        }

        stage('Static Analysis - SonarQube') {
            steps {
                withSonarQubeEnv('SonarQubeServer') {
                    sh './$VENV_DIR/bin/pip install sonar-scanner'
                    sh 'sonar-scanner -Dsonar.projectKey=your_project -Dsonar.sources=. -Dsonar.python.version=3'
                }
            }
        }

        stage('Security Scans') {
            steps {
                sh './$VENV_DIR/bin/pip install bandit safety'
                sh './$VENV_DIR/bin/bandit -r .'
                sh './$VENV_DIR/bin/safety check'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t yourapp:latest .'
            }
        }

        stage('Deploy with Docker') {
            steps {
                sh 'docker run -d -p 8000:8000 yourapp:latest'
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}