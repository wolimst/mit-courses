pipeline {
    agent any
    stages {
        stage('Setup') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Style Check') {
            steps {
                sh 'flake8 .'
            }
        }
        stage('Unit Test') {
            steps {
                sh 'pytest .'
            }
        }
    }
}
