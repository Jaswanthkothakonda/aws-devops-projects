pipeline {
    agent any

    options {
        skipDefaultCheckout(true)
    }

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

        stage('Clean Workspace') {
            steps {
                echo 'Cleaning Jenkins workspace...'
                cleanWs()
            }
        }

        stage('Checkout SCM') {
            steps {
                echo 'Checking out source code from GitHub...'
                checkout scm
            }
        }

        stage('Build Info') {
            steps {
                script {
                    env.GIT_COMMIT_SHORT = sh(
                        script: 'git rev-parse --short HEAD',
                        returnStdout: true
                    ).trim()
                }

                sh '''
                    echo "===== BeastEats CI Pipeline ====="
                    echo "Build Number: ${BUILD_NUMBER}"
                    echo "Environment: ${ENVIRONMENT}"
                    echo "Image Tag: ${IMAGE_TAG}"
                    echo "Git Commit: ${GIT_COMMIT_SHORT}"
                '''
            }
        }

        stage('Generate Build Artifact') {
            steps {
                sh '''
                    echo "===== Build Artifact ====="

                    cat > build-info.txt <<EOF2
BeastEats Build Information
===========================
Build Number: ${BUILD_NUMBER}
Environment: ${ENVIRONMENT}
Image Tag: ${IMAGE_TAG}
Git Commit: $(git rev-parse HEAD)
Short Commit: ${GIT_COMMIT_SHORT}
Build Time: $(date)
EOF2

                    cat build-info.txt
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

        stage('Credential Masking Test') {
            steps {
                withCredentials([
                    string(
                        credentialsId: 'beasteats-secret-test',
                        variable: 'TRAINING_SECRET'
                    )
                ]) {
                    sh '''
                        echo "===== Credential Masking Test ====="
                        echo "Secret value passed to Jenkins:"
                        echo "${TRAINING_SECRET}"
                        echo "Credential masking test complete."
                    '''
                }
            }
        }

        stage('Docker Build') {
            steps {
                sh '''
                    echo "Building BeastEats for ${ENVIRONMENT}"

                    cd docker

                    docker build \
                        -t ${ECR_REPOSITORY}:${IMAGE_TAG} \
                        -t ${ECR_REPOSITORY}:${IMAGE_TAG}-${GIT_COMMIT_SHORT} \
                        .
                '''
            }
        }

        stage('Docker Test') {
            steps {
                sh '''
                    echo "Testing Docker image..."

                    mkdir -p test-results

                    if docker run --rm \
                        ${ECR_REPOSITORY}:${IMAGE_TAG} \
                        nginx -t > nginx-test.log 2>&1
                    then
                        STATUS="PASSED"
                        echo "Docker/Nginx test passed."
                    else
                        STATUS="FAILED"
                        echo "Docker/Nginx test failed."
                        cat nginx-test.log
                    fi

                    if [ "${STATUS}" = "PASSED" ]; then
                        FAILURE_COUNT=0
                    else
                        FAILURE_COUNT=1
                    fi

                    cat > test-results/nginx-test.xml <<EOF2
<?xml version="1.0" encoding="UTF-8"?>
<testsuite name="BeastEats Docker Tests" tests="1" failures="${FAILURE_COUNT}" errors="0" skipped="0">
    <testcase classname="BeastEats.Docker" name="nginx configuration test">
EOF2

                    if [ "${STATUS}" = "FAILED" ]; then
                        cat >> test-results/nginx-test.xml <<EOF2
        <failure message="nginx configuration test failed">
$(cat nginx-test.log)
        </failure>
EOF2
                    fi

                    cat >> test-results/nginx-test.xml <<EOF2
    </testcase>
</testsuite>
EOF2

                    cat test-results/nginx-test.xml

                    if [ "${STATUS}" = "FAILED" ]; then
                        exit 1
                    fi
                '''
            }
        }

        stage('Publish Test Results') {
            steps {
                junit 'test-results/*.xml'
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
                    echo "Pushing BeastEats images to ECR..."

                    docker tag \
                        ${ECR_REPOSITORY}:${IMAGE_TAG} \
                        ${ECR_REGISTRY}/${ECR_REPOSITORY}:${IMAGE_TAG}

                    docker tag \
                        ${ECR_REPOSITORY}:${IMAGE_TAG}-${GIT_COMMIT_SHORT} \
                        ${ECR_REGISTRY}/${ECR_REPOSITORY}:${IMAGE_TAG}-${GIT_COMMIT_SHORT}

                    docker push \
                        ${ECR_REGISTRY}/${ECR_REPOSITORY}:${IMAGE_TAG}

                    docker push \
                        ${ECR_REGISTRY}/${ECR_REPOSITORY}:${IMAGE_TAG}-${GIT_COMMIT_SHORT}
                '''
            }
        }

        stage('Verify ECR') {
            steps {
                sh '''
                    echo "Verifying build-number image..."

                    aws ecr describe-images \
                        --repository-name ${ECR_REPOSITORY} \
                        --image-ids imageTag=${IMAGE_TAG} \
                        --region ${AWS_REGION}

                    echo "Verifying commit-tagged image..."

                    aws ecr describe-images \
                        --repository-name ${ECR_REPOSITORY} \
                        --image-ids imageTag=${IMAGE_TAG}-${GIT_COMMIT_SHORT} \
                        --region ${AWS_REGION}
                '''
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
    }

    post {

        success {
            echo "========================================"
            echo "BEASTEATS PIPELINE SUCCESS"
            echo "========================================"
            echo "Environment: ${ENVIRONMENT}"
            echo "Image: ${ECR_REGISTRY}/${ECR_REPOSITORY}:${IMAGE_TAG}"
            echo "Commit Image: ${ECR_REGISTRY}/${ECR_REPOSITORY}:${IMAGE_TAG}-${GIT_COMMIT_SHORT}"

            archiveArtifacts artifacts: 'build-info.txt', fingerprint: true
        }

        failure {
            echo "========================================"
            echo "BEASTEATS PIPELINE FAILED"
            echo "========================================"
            echo "Environment: ${ENVIRONMENT}"
        }

        aborted {
            echo "========================================"
            echo "BEASTEATS PIPELINE ABORTED"
            echo "========================================"
            echo "Environment: ${ENVIRONMENT}"
        }

        always {
            sh '''
                echo "Cleaning local Docker images..."

                docker image rm \
                    ${ECR_REGISTRY}/${ECR_REPOSITORY}:${IMAGE_TAG} \
                    ${ECR_REGISTRY}/${ECR_REPOSITORY}:${IMAGE_TAG}-${GIT_COMMIT_SHORT} \
                    ${ECR_REPOSITORY}:${IMAGE_TAG} \
                    ${ECR_REPOSITORY}:${IMAGE_TAG}-${GIT_COMMIT_SHORT} \
                    2>/dev/null || true
            '''
        }
    }
}
