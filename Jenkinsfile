pipeline {

    agent any

    environment {
        SERVICE_NAME = "python-api"
        REMOTE_DIR = "/tmp/build-${BUILD_NUMBER}"
        SCRIPT_PATH = "/app/shellscript/compiler.sh"
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
                        script: 'git describe --tags --exact-match || echo latest',
                        returnStdout: true
                    ).trim()
                }
            }
        }

        stage('Build on EC2') {
            steps {
                sshagent(['ec2-prod']) {

                    sh """
                        ssh -o StrictHostKeyChecking=no ec2-user@\$EC2_HOST '
                            rm -rf ${REMOTE_DIR} &&
                            mkdir -p ${REMOTE_DIR}
                        '

                        scp Dockerfile entrypoint.sh test-py.py ec2-user@\$EC2_HOST:${REMOTE_DIR}/

                        ssh ec2-user@\$EC2_HOST '
                            cd ${REMOTE_DIR} &&
                            bash ${SCRIPT_PATH} "${TAG_NAME}" "${SERVICE_NAME}" docker
                        '
                    """
                }
            }
        }
    }
}
