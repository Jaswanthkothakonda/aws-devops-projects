pipeline {
    agent any

    environment {
        AWS_REGION = 'ap-south-2'
        ECR_REGISTRY = '734648185802.dkr.ecr.ap-south-2.amazonaws.com'
        ECR_REPOSITORY = 'beasteats'
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {

        stage('Build Info') {
            steps {
                sh '''
                    echo "===== BeastEats CI Pipeline ====="
                    echo "Build Number: ${BUILD_NUMBER}"
                    echo "Image Tag: ${IMAGE_TAG}"
                    echo "Git Commit:"
                    git log -1 --oneline
                '''
            }
        }

        stage('Docker Build') {
            steps {
                sh '''
                    cd docker

                    docker build \
                        -t ${ECR_REPOSITORY}:${IMAGE_TAG} .
                '''
            }
        }

        stage('Docker Test') {
            steps {
                sh '''
                    docker run --rm ${ECR_REPOSITORY}:${IMAGE_TAG} nginx -t
                '''
            }
        }

        stage('ECR Login') {
            steps {
                sh '''
                    aws ecr get-login-password \
                        --region ${AWS_REGION} | \
                    docker login \
                        --username AWS \
                        --password-stdin ${ECR_REGISTRY}
                '''
            }
        }

        stage('Push to ECR') {
            steps {
                sh '''
                    docker tag \
                        ${ECR_REPOSITORY}:${IMAGE_TAG} \
                        ${ECR_REGISTRY}/${ECR_REPOSITORY}:${IMAGE_TAG}

                    docker push \
                        ${ECR_REGISTRY}/${ECR_REPOSITORY}:${IMAGE_TAG}
                '''
            }
        }

        stage('Verify ECR') {
            steps {
                sh '''
                    aws ecr describe-images \
                        --repository-name ${ECR_REPOSITORY} \
                        --image-ids imageTag=${IMAGE_TAG} \
                        --region ${AWS_REGION}
                '''
            }
        }
    }

    post {
        success {
            echo 'BeastEats CI pipeline completed successfully.'
        }

        failure {
            echo 'BeastEats CI pipeline failed.'
        }

        always {
            sh '''
                docker image rm \
                    ${ECR_REGISTRY}/${ECR_REPOSITORY}:${IMAGE_TAG} \
                    ${ECR_REPOSITORY}:${IMAGE_TAG} \
                    2>/dev/null || true
            '''
        }
    }
}
