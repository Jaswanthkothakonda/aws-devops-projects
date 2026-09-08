pipeline {
    agent any

    stages {
        stage('Build Info') {
            steps {
                sh '''
                    echo "===== BeastEats CI Pipeline ====="
                    echo "Build Number: ${BUILD_NUMBER}"
                    echo "Workspace: ${WORKSPACE}"
                    echo "Git Commit:"
                    git log -1 --oneline
                '''
            }
        }

        stage('Docker Build') {
            steps {
                sh '''
                    cd docker
                    docker build -t beasteats:${BUILD_NUMBER} .
                '''
            }
        }

        stage('Docker Test') {
            steps {
                sh '''
                    docker run --rm beasteats:${BUILD_NUMBER} nginx -t
                '''
            }
        }

        stage('ECR Login') {
            steps {
                sh '''
                    aws ecr get-login-password --region ap-south-2 | \
                    docker login --username AWS --password-stdin \
                    734648185802.dkr.ecr.ap-south-2.amazonaws.com
                '''
            }
        }

        stage('Push to ECR') {
            steps {
                sh '''
                    docker tag beasteats:${BUILD_NUMBER} \
                    734648185802.dkr.ecr.ap-south-2.amazonaws.com/beasteats:${BUILD_NUMBER}

                    docker push \
                    734648185802.dkr.ecr.ap-south-2.amazonaws.com/beasteats:${BUILD_NUMBER}
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
    }
}
