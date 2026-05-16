pipeline {

    agent any

    environment {

        SERVICE_NAME = "python-api"

        HARBOR_URL = "http://ec2-54-179-57-101.ap-southeast-1.compute.amazonaws.com:8080"
    }

    stages {

        stage('Checkout') {

            steps {
                checkout scm
            }
        }

        stage('Get Git Tag') {

            steps {

                script {

                    env.TAG_NAME = sh(
                        script: 'git describe --tags --exact-match || echo latest',
                        returnStdout: true
                    ).trim()

                    echo "Tag Name: ${env.TAG_NAME}"
                }
            }
        }

        stage('Pull Config') {

            steps {

                sh """
                    chmod +x /app/shellscript/compiler.sh

                    /app/shellscript/compiler.sh \
                    ${TAG_NAME} \
                    ${SERVICE_NAME} \
                    pc
                """
            }
        }

        stage('Docker Build & Push') {

            steps {

                sh """
                    chmod +x /app/shellscript/compiler.sh

                    /app/shellscript/compiler.sh \
                    ${TAG_NAME} \
                    ${SERVICE_NAME} \
                    docker
                """
            }
        }
    }

    post {

        always {

            deleteDir()
        }

        success {

            echo 'Pipeline completed successfully.'
        }

        failure {

            echo 'Pipeline failed.'
        }
    }
}
