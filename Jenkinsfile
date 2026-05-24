pipeline {

    agent any

    options {
        overrideIndexTriggers(true)
    }

    environment {
        SERVICE_NAME = "python-api"
        REMOTE_DIR = "/tmp/build-${BUILD_NUMBER}"
    }

    stages {

        stage('Debug') {
            steps {
                sh '''
                echo "BRANCH_NAME=$BRANCH_NAME"
                echo "TAG_NAME=$TAG_NAME"
                '''
            }
        }

        stage('Check Tag') {
            when {
                buildingTag()
            }

            steps {
                script {
                    env.IMAGE_TAG = env.TAG_NAME
                    echo "Building tag: ${env.IMAGE_TAG}"
                }
            }
        }

        stage('Checkout') {
            when {
                buildingTag()
            }

            steps {
                checkout scm
            }
        }

        stage('Build on EC2') {

            when {
                buildingTag()
            }

            steps {

                withCredentials([
                    file(
                        credentialsId: 'ec2-pem-file',
                        variable: 'PEM'
                    ),
                    string(
                        credentialsId: 'ec2-host',
                        variable: 'EC2_HOST'
                    )
                ]) {

                    sh '''
                    chmod 400 "$PEM"

                    ssh -i "$PEM" \
                    -o StrictHostKeyChecking=no \
                    ec2-user@$EC2_HOST "
                        rm -rf ${REMOTE_DIR}
                        mkdir -p ${REMOTE_DIR}
                    "

                    scp -i "$PEM" \
                    test-py.py \
                    ec2-user@$EC2_HOST:${REMOTE_DIR}/

                    ssh -i "$PEM" \
                    ec2-user@$EC2_HOST "
                        bash /app/shellscript/compiler.sh \
                        ${IMAGE_TAG} \
                        ${SERVICE_NAME} \
                        ${REMOTE_DIR}
                    "
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "Build completed: ${IMAGE_TAG}"
        }

        failure {
            echo "Build failed"
        }
    }
}
