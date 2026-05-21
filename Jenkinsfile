pipeline {

    agent any

    environment {
        SERVICE_NAME = "python-api"
        REMOTE_DIR="/tmp/build-${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Get Tag') {
            steps {
                script {

                    env.TAG_NAME = sh(
                        script: '''
                        git describe --tags --exact-match 2>/dev/null || echo latest
                        ''',
                        returnStdout: true
                    ).trim()

                    echo "Tag=${env.TAG_NAME}"
                }
            }
        }

        stage('Build on EC2') {

            steps {

                withCredentials([
                    file(
                        credentialsId:'ec2-pem-file',
                        variable:'PEM'
                    ),
                    string(
                        credentialsId:'ec2-host',
                        variable:'EC2_HOST'
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
                    ${TAG_NAME} \
                    ${SERVICE_NAME} \
                    ${REMOTE_DIR}
                    "
                    '''
                }
            }
        }
    }
}
