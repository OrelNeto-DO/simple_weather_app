pipeline {
    agent any
    
    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
        DOCKER_IMAGE = 'simple_weather_app'
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
                        docker build -t $DOCKERHUB_CREDENTIALS_USR/$DOCKER_IMAGE:$BUILD_NUMBER .
                    '''
                }
            }
        }
        
        stage('Test') {
            steps {
                script {
                    sh '''
                        docker run -d --name weather_test_${BUILD_NUMBER} $DOCKERHUB_CREDENTIALS_USR/$DOCKER_IMAGE:$BUILD_NUMBER
                        sleep 10
                        docker ps | grep weather_test_${BUILD_NUMBER}
                        docker stop weather_test_${BUILD_NUMBER}
                        docker rm weather_test_${BUILD_NUMBER}
                    '''
                }
            }
        }
        
        stage('Push to DockerHub') {
            steps {
                script {
                    sh '''
                        docker push $DOCKERHUB_CREDENTIALS_USR/$DOCKER_IMAGE:$BUILD_NUMBER
                    '''
                }
            }
        }
    }
    
    post {
        always {
            script {
                sh '''
                    docker rmi $DOCKERHUB_CREDENTIALS_USR/$DOCKER_IMAGE:$BUILD_NUMBER || true
                    docker logout
                '''
            }
        }
    }
}
