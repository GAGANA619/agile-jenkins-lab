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

                bat '"C:\\Users\\Gagana\\AppData\\Local\\Python\\pythoncore-3.14-64\\python.exe" loan_processing_qa.py'
            }
        }

        stage('Pipeline Completed') {
            steps {
                echo '===== BANKING LOAN PIPELINE PASSED ====='
            }
        }
    }

    post {

        success {
            echo '===== CI PIPELINE SUCCESS ====='
        }

        failure {
            echo '===== CI PIPELINE FAILED ====='
        }
    }
}
