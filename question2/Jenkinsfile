pipeline {

    agent any

    stages {

        stage('Checkout') {
            steps {
                echo '===== E-COMMERCE ORDER PROCESSING ====='
                echo 'Code checkout completed'
            }
        }

        stage('Run QA Tests') {
            steps {
                echo '===== RUNNING E-COMMERCE QA TESTS ====='

                bat '"C:\\Users\\Gagana\\AppData\\Local\\Python\\pythoncore-3.14-64\\python.exe" order_management_qa.py'
            }
        }

        stage('Application Test') {
            steps {
                echo '===== E-COMMERCE APPLICATION TEST ====='

                bat '"C:\\Users\\Gagana\\AppData\\Local\\Python\\pythoncore-3.14-64\\python.exe" -c "import order_management; print(\'Application module loaded successfully\')"'
            }
        }

        stage('Pipeline Completed') {
            steps {
                echo '===== E-COMMERCE PIPELINE PASSED ====='
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