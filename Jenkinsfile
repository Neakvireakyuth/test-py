pipeline {

    agent any

    environment {

        SERVICE_NAME = "python-api"

        HARBOR_URL = "10.0.200.204:7200"
    }

    stages {

        stage('Checkout') {

            steps {

                checkout scm

                sh 'git fetch --tags'
            }
        }

        stage('Get Git Tag') {

            steps {

                script {

                    env.TAG_NAME = sh(
                        script: '''
                            git describe --tags --exact-match 2>/dev/null || echo latest
                        ''',
                        returnStdout: true
                    ).trim()

                    echo "Detected Tag: ${env.TAG_NAME}"
                }
            }
        }

        stage('Pull Config') {

            steps {

                sh '''
                    chmod +x compiler.sh
                    ./compiler.sh ${TAG_NAME} ${SERVICE_NAME} pc
                '''
            }
        }

        stage('Docker Build & Push') {

            when {

                expression {

                    return env.TAG_NAME != "latest"
                }
            }

            steps {

                sh '''
                    ./compiler.sh ${TAG_NAME} ${SERVICE_NAME} docker
                '''
            }
        }
    }

    post {

        success {

            echo 'Pipeline completed successfully.'
        }

        failure {

            echo 'Pipeline failed.'
        }

        always {

            cleanWs()
        }
    }
}
