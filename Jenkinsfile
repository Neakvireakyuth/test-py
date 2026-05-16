pipeline {

    agent any

    environment {

        SERVICE_NAME = "python-api"

        HARBOR_URL = "ec2-54-179-57-101.ap-southeast-1.compute.amazonaws.com:8080"
    }

    stages {

        stage('Checkout') {

            steps {

                checkout scm
            }
        }

        stage('Debug Workspace') {

            steps {

                sh '''
                    echo "===== WORKSPACE ====="
                    pwd

                    echo "===== FILES ====="
                    ls -la

                    echo "===== SCRIPT CHECK ====="
                    ls -la /app/shellscript

                    echo "===== CONFIG CHECK ====="
                    ls -la /opt/configs
                '''
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
