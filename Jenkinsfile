pipeline {
    agent any

    triggers {
        githubPush()
    }

    environment {
        SERVICE_NAME = "python-api"
        REMOTE_DIR = "/tmp/build-${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Get Tag') {
            when {
                buildingTag()
            }

            steps {
                script {
                    env.TAG_NAME = env.TAG_NAME

                    echo "Tag: ${env.TAG_NAME}"
                }
            }
        }

        stage('Build on EC2') {
            when {
                buildingTag()
            }

            steps {

                withCredentials([
                    file(credentialsId: 'ec2-pem-file', variable: 'PEM'),
                    string(credentialsId: 'ec2-host', variable: 'EC2_HOST')
                ]) {

                    sh '''
                    chmod 400 "$PEM"

                    ssh -i "$PEM" -o StrictHostKeyChecking=no ec2-user@$EC2_HOST "
                        rm -rf ${REMOTE_DIR}
                        mkdir -p ${REMOTE_DIR}
                    "

                    scp -i "$PEM" test-py.py \
                    ec2-user@$EC2_HOST:${REMOTE_DIR}/

                    ssh -i "$PEM" ec2-user@$EC2_HOST "
                        cd ${REMOTE_DIR}

                        bash /app/shellscript/compiler.sh ${TAG_NAME} ${SERVICE_NAME} pc

                        bash /app/shellscript/compiler.sh ${TAG_NAME} ${SERVICE_NAME} docker
                    "
                    '''
                }
            }
        }
    }
}
