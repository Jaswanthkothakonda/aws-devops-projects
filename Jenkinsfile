pipeline {
    agent any

    parameters {
        choice(
            name: 'ENVIRONMENT',
            choices: ['dev', 'staging', 'production'],
            description: 'Deployment environment for BeastEats'
        )
    }

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
                    echo "Environment: ${ENVIRONMENT}"
                    echo "Image Tag: ${IMAGE_TAG}"
                    echo "Git Commit:"
                    git log -1 --oneline
                '''
            }
        }

        stage('Environment Check') {
            steps {
                script {
                    if (env.ENVIRONMENT == 'dev') {
                        echo 'Development environment selected.'
                    } else if (env.ENVIRONMENT == 'staging') {
                        echo 'Staging environment selected.'
                    } else if (env.ENVIRONMENT == 'production') {
                        echo 'Production environment selected.'
                    }
                }
            }
        }
stage('Dev Environment Action') {
    when {
        environment name: 'ENVIRONMENT', value: 'dev'
    }
    steps {
        echo 'Running development-specific action.'
    }
}

stage('Staging Environment Action') {
    when {
        environment name: 'ENVIRONMENT', value: 'staging'
    }
    steps {
        echo 'Running staging-specific action.'
    }
}

stage('Production Environment Action') {
    when {
        environment name: 'ENVIRONMENT', value: 'production'
    }
    steps {
        echo 'Running production-specific action.'
    }
}

        stage('Docker Build') {
            steps {
                sh '''
                    echo "Building BeastEats for ${ENVIRONMENT}"

                    cd docker

                    docker build \
                        -t ${ECR_REPOSITORY}:${IMAGE_TAG} .
                '''
            }
        }

        stage('Docker Test') {
            steps {
                sh '''
                    echo "Testing Docker image..."

                    docker run --rm \
                        ${ECR_REPOSITORY}:${IMAGE_TAG} \
                        nginx -t
                '''
            }
        }

        stage('ECR Login') {
            steps {
                sh '''
                    echo "Logging in to Amazon ECR..."

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
                    echo "Pushing ${ECR_REPOSITORY}:${IMAGE_TAG} to ECR..."

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
                    echo "Verifying image in ECR..."

                    aws ecr describe-images \
                        --repository-name ${ECR_REPOSITORY} \
                        --image-ids imageTag=${IMAGE_TAG} \
                        --region ${AWS_REGION}
                '''
            }
        }
    }
stage('Production Approval') {
    when {
        environment name: 'ENVIRONMENT', value: 'production'
    }

    steps {
        input(
            message: 'Approve BeastEats production release?',
            ok: 'Approve Release'
        )
    }
}

    post {
        success {
            echo "BeastEats CI pipeline completed successfully."
            echo "Environment: ${ENVIRONMENT}"
            echo "Image: ${ECR_REGISTRY}/${ECR_REPOSITORY}:${IMAGE_TAG}"
        }

        failure {
            echo "BeastEats CI pipeline failed."
            echo "Environment: ${ENVIRONMENT}"
        }

        always {
            sh '''
                echo "Cleaning local Docker images..."

                docker image rm \
                    ${ECR_REGISTRY}/${ECR_REPOSITORY}:${IMAGE_TAG} \
                    ${ECR_REPOSITORY}:${IMAGE_TAG} \
                    2>/dev/null || true
            '''
        }
    }
}
