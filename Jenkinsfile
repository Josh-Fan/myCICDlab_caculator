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
                powershell '''
                    python -m venv $env:VENV_DIR
                    .\\$env:VENV_DIR\\Scripts\\Activate.ps1
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Static Analysis - SonarQube') {
            steps {
                withSonarQubeEnv('SonarQubeServer') {
                    powershell '''
                        .\\$env:VENV_DIR\\Scripts\\Activate.ps1
                        pip install sonar-scanner
                        sonar-scanner -Dsonar.projectKey=your_project -Dsonar.sources=. -Dsonar.python.version=3
                    '''
                }
            }
        }

        stage('Security Scans') {
            steps {
                powershell '''
                    .\\$env:VENV_DIR\\Scripts\\Activate.ps1
                    pip install bandit safety
                    bandit -r .
                    safety check
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                powershell 'docker build -t yourapp:latest .'
            }
        }

        stage('Deploy with Docker') {
            steps {
                powershell 'docker run -d -p 8000:8000 yourapp:latest'
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
