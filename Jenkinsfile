pipeline {
    agent any
    
    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
        DOCKER_REPO = 'orelneto/simple_weather_app'
    }
    
    stages {
        stage('Cleanup') {
            steps {
                // Clean workspace before build
                cleanWs()
            }
        }
        
        stage('Copy Repository') {
            steps {
                // Clone the repository
                git branch: 'main',
                    url: 'https://github.com/OrelNeto-DO/simple_weather_app.git'
            }
        }
        
        stage('Build') {
            steps {
                script {
                    // Build the Docker image
                    dockerImage = docker.build("${DOCKER_REPO}:${BUILD_NUMBER}")
                    // Also tag as latest
                    dockerImage.tag("latest")
                }
            }
        }
        
        stage('Test') {
            steps {
                script {
                    // Run the container and test it
                    sh """
                        docker run -d --name weather_test_${BUILD_NUMBER} ${DOCKER_REPO}:${BUILD_NUMBER}
                        # Wait for container to start
                        sleep 10
                        # Check if container is running
                        docker ps | grep weather_test_${BUILD_NUMBER}
                        # Stop and remove the test container
                        docker stop weather_test_${BUILD_NUMBER}
                        docker rm weather_test_${BUILD_NUMBER}
                    """
                }
            }
        }
        
        stage('Push to DockerHub') {
            steps {
                script {
                    // Login to DockerHub
                    sh "echo \$DOCKERHUB_CREDENTIALS_PSW | docker login -u \$DOCKERHUB_CREDENTIALS_USR --password-stdin"
                    
                    // Push both tags
                    sh "docker push ${DOCKER_REPO}:${BUILD_NUMBER}"
                    sh "docker push ${DOCKER_REPO}:latest"
                    
                    // Logout from DockerHub
                    sh "docker logout"
                }
            }
        }
    }
    
    post {
        always {
            // Clean up Docker images
            script {
                sh "docker rmi ${DOCKER_REPO}:${BUILD_NUMBER}"
                sh "docker rmi ${DOCKER_REPO}:latest"
            }
        }
    }
}
