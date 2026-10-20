pipeline {
    agent any

    environment {
        PYTHONUNBUFFERED = '1'
    }

    stages {
        stage('SCM Checkout') {
            steps {
                echo 'Checking out source code from GitHub repository...'
                checkout scm
            }
        }

        stage('Environment Setup & Dependencies') {
            steps {
                echo 'Creating virtual environment and installing packages...'
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Code Linting & Syntax Gate') {
            steps {
                echo 'Running static syntax checks with Flake8...'
                sh '''
                    . venv/bin/activate
                    flake8 app/ database/ --count --select=E9,F63,F7,F82 --show-source --statistics
                '''
            }
        }

        stage('Automated Unit & Integration Tests') {
            steps {
                echo 'Running Pytest suites and exporting JUnit XML report...'
                sh '''
                    . venv/bin/activate
                    mkdir -p reports
                    pytest -v --cov=app --junitxml=reports/test-results.xml tests/
                '''
            }
        }
    }

    post {
        always {
            echo 'Archiving test execution reports...'
            junit allowEmptyResults: true, testResults: 'reports/test-results.xml'
            cleanWs deleteDirs: true, notFailBuild: true
        }
        success {
            echo "CI pipeline succeeded for build #${BUILD_NUMBER}!"
        }
        failure {
            echo "Build #${BUILD_NUMBER} FAILED! Inspect the console log for the root cause."
        }
    }
}
