pipeline {

    agent any

    stages {

        stage('Checkout') {
            steps {
                echo '===== BANKING LOAN SYSTEM ====='
                echo 'Code checkout completed'
            }
        }

        stage('Run QA Tests') {
            steps {
                echo '===== RUNNING QA TESTS ====='
                bat 'python loanprocessing_qa.py'
            }
        }

        stage('Application Test') {
            steps {
                echo '===== APPLICATION TEST ====='
                bat 'python -c "import loanprocessing; print(\\'Application module loaded successfully\\')"'
            }
        }
    }

    post {

        success {
            echo '===== BANKING LOAN PIPELINE PASSED ====='
        }

        failure {
            echo '===== BANKING LOAN PIPELINE FAILED ====='
        }
    }
}