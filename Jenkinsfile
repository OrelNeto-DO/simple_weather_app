pipeline {
    agent any
    
    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
        AWS_EC2_CREDENTIALS = credentials('aws-ec2-credentials')
        DOCKER_IMAGE = 'simple_weather_app'
        APP_PORT = '5000'
        VERSION = "1.0.${BUILD_NUMBER}"
        EC2_INSTANCE_IP = '3.82.55.186'  // Replace with relevant EC2 IP
        EC2_USER = 'ec2-user'  // Amazon Linux uses ec2-user as default
    }
    
    stages {
        stage('Cleanup') {
            steps {
                cleanWs()
            }
        }
        
        stage('Copy Repository') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/OrelNeto-DO/simple_weather_app.git'
            }
        }
        
        stage('Docker Login') {
            steps {
                script {
                    sh '''
                        echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin
                    '''
                }
            }
        }
        
        stage('Build') {
            steps {
                script {
                    sh '''
                        # Build with version tag
                        docker build -t $DOCKERHUB_CREDENTIALS_USR/$DOCKER_IMAGE:$VERSION .
                        # Tag as latest
                        docker tag $DOCKERHUB_CREDENTIALS_USR/$DOCKER_IMAGE:$VERSION $DOCKERHUB_CREDENTIALS_USR/$DOCKER_IMAGE:latest
                    '''
                }
            }
        }
        
        stage('Push to DockerHub') {
            steps {
                script {
                    sh '''
                        # Push version tag
                        docker push $DOCKERHUB_CREDENTIALS_USR/$DOCKER_IMAGE:$VERSION
                        # Push latest tag
                        docker push $DOCKERHUB_CREDENTIALS_USR/$DOCKER_IMAGE:latest
                    '''
                }
            }
        }

        stage('Deploy to EC2') {
            steps {
                script {
                    sshagent(['aws-ec2-credentials']) {
                        sh """
                            ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_INSTANCE_IP} '
                                # Install Docker if not present
                                if ! command -v docker &> /dev/null; then
                                    sudo yum update -y
                                    sudo yum install -y docker
                                    sudo service docker start
                                    sudo usermod -a -G docker ${EC2_USER}
                                fi

                                # Pull the latest image
                                docker pull ${DOCKERHUB_CREDENTIALS_USR}/${DOCKER_IMAGE}:latest

                                # Stop and remove existing container if exists
                                docker stop ${DOCKER_IMAGE} || true
                                docker rm ${DOCKER_IMAGE} || true

                                # Run new container
                                docker run -d --name ${DOCKER_IMAGE} -p ${APP_PORT}:${APP_PORT} ${DOCKERHUB_CREDENTIALS_USR}/${DOCKER_IMAGE}:latest
                            '
                        """
                    }
                }
            }
        }

        stage('Verify Deployment') {
            steps {
                script {
                    sh """
                        # Wait for application to start
                        sleep 20
                        
                        # Test if application is responding
                        curl -f http://${EC2_INSTANCE_IP}:${APP_PORT} || exit 1
                        
                        echo "Application is successfully deployed and accessible at http://${EC2_INSTANCE_IP}:${APP_PORT}"
                    """
                }
            }
        }
    }
    
    post {
        always {
            script {
                sh '''
                    # Remove both version and latest tags locally
                    docker rmi $DOCKERHUB_CREDENTIALS_USR/$DOCKER_IMAGE:$VERSION || true
                    docker rmi $DOCKERHUB_CREDENTIALS_USR/$DOCKER_IMAGE:latest || true
                    docker logout
                '''
            }
        }
        success {
            echo "Deployment successful! Application is running at http://${EC2_INSTANCE_IP}:${APP_PORT}"
        }
        failure {
            echo 'Deployment failed! Check the logs for details.'
        }
    }
}
