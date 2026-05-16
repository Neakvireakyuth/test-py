pipeline {
    agent any

    environment {
        SERVICE_NAME = "python-api"
        REMOTE_DIR = "/tmp/build-${BUILD_NUMBER}"
    }

    stages {

        stage('Deploy') {
            steps {
                withCredentials([
                    file(credentialsId: 'ec2-pem-file', variable: 'PEM'),
                    string(credentialsId: 'ec2-host', variable: 'EC2_HOST')
                ]) {

                    withEnv(["EC2_HOST=${EC2_HOST}"]) {

                        sh '''
                            chmod 400 "$PEM"

                            ssh -i "$PEM" -o StrictHostKeyChecking=no ec2-user@$EC2_HOST "
                                rm -rf /tmp/build && mkdir -p /tmp/build
                            "

                            scp -i "$PEM" Dockerfile entrypoint.sh test-py.py \
                                ec2-user@$EC2_HOST:/tmp/build/

                            ssh -i "$PEM" ec2-user@$EC2_HOST "
                                cd /tmp/build &&
                                bash /app/shellscript/compiler.sh latest python-api docker
                            "
                        '''
                    }
                }
            }
        }
    }
}
