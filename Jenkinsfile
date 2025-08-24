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
                    python -m venv "$env:VENV_DIR"
                    $activateScript = Join-Path $env:VENV_DIR "Scripts\\Activate.ps1"
                    if (Test-Path $activateScript) {
                        & $activateScript
                        pip install -r requirements.txt
                        python.exe -m pip install --upgrade pip
                    } else {
                        Write-Error "Activation script not found at $activateScript"
                        exit 1
                    }
                '''
            }
        }

        stage('SonarQube Scan') {
            steps {
                withSonarQubeEnv('SonarQubeServer') {
                    powershell '''
                    sonar-scanner `
                    -D sonar.projectKey="my1stscan" `
                    -D sonar.sources="." `
                    -D sonar.python.version="3.13"
                    '''
                }
            }
        }

        stage('Security Scans') {
            steps {
                powershell '''
                    $activateScript = Join-Path $env:VENV_DIR "Scripts\\Activate.ps1"
                    if (Test-Path $activateScript) {
                        & $activateScript
                        pip install bandit safety
                        bandit -r .  --disable-parser -f json -o bandit_report.json
                        safety scan --output text
                    } else {
                        Write-Error "Activation script not found at $activateScript"
                        exit 1
                    }
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
