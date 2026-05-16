pipeline {
    agent any

    environment {
        EC2_HOST = "172.31.40.132"
        SERVICE_NAME = "python-api"
        REMOTE_DIR = "/tmp/build-${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Deploy via SSH using PEM file') {
            steps {
                withCredentials([file(credentialsId: 'ec2-pem-file', variable: 'PEM')]) {

                    sh """
                        chmod 400 $PEM

                        ssh -i $PEM -o StrictHostKeyChecking=no ec2-user@${EC2_HOST} '
                            rm -rf ${REMOTE_DIR} &&
                            mkdir -p ${REMOTE_DIR}
                        '

                        scp -i $PEM Dockerfile entrypoint.sh test-py.py \
                            ec2-user@${EC2_HOST}:${REMOTE_DIR}/

                        ssh -i $PEM ec2-user@${EC2_HOST} '
                            cd ${REMOTE_DIR} &&
                            bash /app/shellscript/compiler.sh latest ${SERVICE_NAME} docker
                        '
                    """
                }
            }
        }
    }
}
