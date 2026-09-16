pipeline {
    agent any

    environment {
        IMAGE_NAME = "manoj99eng/aws-devops-app:${BUILD_NUMBER}"
        LATEST_IMAGE = "manoj99eng/aws-devops-app:latest"
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

        stage('Deploy') {
            steps {
                echo "Docker image pushed successfully: ${IMAGE_NAME}"
            }
        }
    }

    post {
        success {
            echo 'CI/CD pipeline completed successfully!'
        }

        failure {
            echo 'Pipeline failed. Check the stage logs.'
        }
    }
}
