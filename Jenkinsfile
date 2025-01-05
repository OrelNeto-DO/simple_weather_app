pipeline {
    agent any
    
    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
        DOCKER_IMAGE = 'simple_weather_app'
        APP_PORT = '5000'
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
                        # Run the container
                        docker run -d -p $APP_PORT:$APP_PORT --name weather_test_${BUILD_NUMBER} $DOCKERHUB_CREDENTIALS_USR/$DOCKER_IMAGE:$BUILD_NUMBER

                        # Wait for application to start
                        echo "Waiting for application to start..."
                        sleep 15

                        # Basic connectivity test
                        echo "Testing basic connectivity..."
                        curl -f http://localhost:$APP_PORT || exit 1
                        
                        # Test homepage content
                        echo "Testing homepage content..."
                        curl -s http://localhost:$APP_PORT | grep "Weather Explorer" || exit 1
                        
                        # Test weather API endpoint (optional, depends on your app structure)
                        # curl -X POST -H "Content-Type: application/x-www-form-urlencoded" -d "city=London&country=UK" http://localhost:$APP_PORT

                        echo "All tests passed successfully!"

                        # Cleanup
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
