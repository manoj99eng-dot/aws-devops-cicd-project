pipeline {
    agent any

    environment {
        IMAGE_NAME  = "manoj99eng/aws-devops-app:${BUILD_NUMBER}"
        LATEST_IMAGE = "manoj99eng/aws-devops-app:latest"
        CONTAINER_NAME = "aws-devops-app"
        APP_PORT = "5000"
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/manoj99eng-dot/aws-devops-cicd-project.git'
            }
        }

        stage('Test') {
            steps {
                sh '''
                    python3 -m venv venv
                    ./venv/bin/pip install -r app/requirements.txt
                    ./venv/bin/python -m py_compile app/app.py
                '''
            }
        }

        stage('Docker Build') {
            steps {
                sh '''
                    docker build \
                        -t ${IMAGE_NAME} \
                        -t ${LATEST_IMAGE} .
                '''
            }
        }

        stage('Docker Login') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'docker-hub-creds',
                        usernameVariable: 'DOCKER_USERNAME',
                        passwordVariable: 'DOCKER_PASSWORD'
                    )
                ]) {
                    sh '''
                        echo "$DOCKER_PASSWORD" | docker login \
                            -u "$DOCKER_USERNAME" \
                            --password-stdin
                    '''
                }
            }
        }

        stage('Docker Push') {
            steps {
                sh '''
                    docker push ${IMAGE_NAME}
                    docker push ${LATEST_IMAGE}
                '''
            }
        }

        stage('Deploy to EC2') {
            steps {
                sh '''
                    echo "Stopping old container..."

                    docker stop ${CONTAINER_NAME} 2>/dev/null || true

                    echo "Removing old container..."

                    docker rm ${CONTAINER_NAME} 2>/dev/null || true

                    echo "Pulling new image..."

                    docker pull ${IMAGE_NAME}

                    echo "Starting new container..."

                    docker run -d \
                        --name ${CONTAINER_NAME} \
                        --restart unless-stopped \
                        -p ${APP_PORT}:5000 \
                        ${IMAGE_NAME}

                    echo "Waiting for application..."

                    sleep 5

                    echo "Checking container status..."

                    docker ps --filter "name=${CONTAINER_NAME}"

                    echo "Testing application health..."

                    curl --fail http://localhost:${APP_PORT}/health

                    echo ""
                    echo "Deployment successful!"
                '''
            }
        }
    }

    post {
        success {
            echo 'CI/CD pipeline completed successfully!'
            echo "Application deployed on EC2 port ${APP_PORT}"
        }

        failure {
            echo 'Pipeline failed. Check the stage logs.'
        }

        always {
            sh 'docker logout || true'
        }
    }
}
