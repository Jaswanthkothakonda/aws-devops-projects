pipeline {
    agent any

    options {
        skipDefaultCheckout(true)
        timeout(time: 30, unit: 'MINUTES')
        disableConcurrentBuilds()
        timestamps()
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
                cleanWs()
            }
        }

        stage('Checkout SCM') {
            steps {
                retry(2) {
                    checkout scm
                }
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
                    echo "Build: ${BUILD_NUMBER}"
                    echo "Environment: ${ENVIRONMENT}"
                    echo "Commit: ${GIT_COMMIT_SHORT}"
                '''
            }
        }

        stage('Validate BeastEats Project') {
            steps {
                sh '''
                    test -f BeastEats/Dockerfile
                    test -f BeastEats/requirements.txt
                    test -f BeastEats/app/__init__.py
                    test -f BeastEats/tests/test_app.py
                    test -f sonar-project.properties
                    echo "BeastEats project validation passed."
                '''
            }
        }

        stage('Generate Build Artifact') {
            steps {
                sh '''
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
                '''
            }
        }

        stage('Environment Check') {
            steps {
                echo "Environment selected: ${ENVIRONMENT}"
            }
        }

        stage('Docker Build') {
            steps {
                sh '''
                    docker build \
                        -t ${ECR_REPOSITORY}:${IMAGE_TAG} \
                        -t ${ECR_REPOSITORY}:${IMAGE_TAG}-${GIT_COMMIT_SHORT} \
                        BeastEats
                '''
            }
        }

        stage('BeastEats Automated Tests') {
            steps {
                sh '''
                    mkdir -p BeastEats/test-results

                    docker run --rm \
                        --user "$(id -u):$(id -g)" \
                        -e PYTHONPATH=/app \
                        -v "$WORKSPACE/BeastEats:/app" \
                        -w /app \
                        ${ECR_REPOSITORY}:${IMAGE_TAG} \
                        pytest \
                            --cov=app \
                            --cov-report=xml:coverage.xml \
                            --junitxml=test-results/pytest-results.xml \
                            tests/
                '''
            }
        }

        stage('Publish Test Results') {
            steps {
                junit 'BeastEats/test-results/*.xml'
                archiveArtifacts(
                    artifacts: 'BeastEats/coverage.xml,BeastEats/test-results/*.xml',
                    fingerprint: true
                )
            }
        }

        stage('SonarCloud Analysis') {
            steps {
                script {
                    def scannerHome = tool 'BeastEatsSonarScanner'

                    withSonarQubeEnv('BeastEatsSonarCloud') {
                        sh """
                            ${scannerHome}/bin/sonar-scanner \
                                -Dproject.settings=sonar-project.properties
                        """
                    }
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    script {
                        def qg = waitForQualityGate()

                        echo "BeastEats Quality Gate Status: ${qg.status}"

                        if (qg.status != 'OK') {
                            error "BeastEats Quality Gate failed: ${qg.status}"
                        }
                    }
                }
            }
        }

        stage('ECR Login') {
            steps {
                retry(2) {
                    sh '''
                        aws ecr get-login-password \
                            --region ${AWS_REGION} |
                        docker login \
                            --username AWS \
                            --password-stdin ${ECR_REGISTRY}
                    '''
                }
            }
        }

        stage('Push to ECR') {
            steps {
                sh '''
                    docker tag \
                        ${ECR_REPOSITORY}:${IMAGE_TAG} \
                        ${ECR_REGISTRY}/${ECR_REPOSITORY}:${IMAGE_TAG}

                    docker tag \
                        ${ECR_REPOSITORY}:${IMAGE_TAG}-${GIT_COMMIT_SHORT} \
                        ${ECR_REGISTRY}/${ECR_REPOSITORY}:${IMAGE_TAG}-${GIT_COMMIT_SHORT}
                '''

                retry(2) {
                    sh '''
                        docker push \
                            ${ECR_REGISTRY}/${ECR_REPOSITORY}:${IMAGE_TAG}
                    '''
                }

                retry(2) {
                    sh '''
                        docker push \
                            ${ECR_REGISTRY}/${ECR_REPOSITORY}:${IMAGE_TAG}-${GIT_COMMIT_SHORT}
                    '''
                }
            }
        }

        stage('Verify ECR') {
            steps {
                sh '''
                    aws ecr describe-images \
                        --repository-name ${ECR_REPOSITORY} \
                        --image-ids imageTag=${IMAGE_TAG} \
                        --region ${AWS_REGION}

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
            echo "BEASTEATS PIPELINE SUCCESS"
            echo "Environment: ${ENVIRONMENT}"
            echo "Image: ${ECR_REGISTRY}/${ECR_REPOSITORY}:${IMAGE_TAG}"
            archiveArtifacts(
                artifacts: 'build-info.txt',
                fingerprint: true
            )
        }

        failure {
            echo "BEASTEATS PIPELINE FAILED"
            echo "Environment: ${ENVIRONMENT}"
        }

        aborted {
            echo "BEASTEATS PIPELINE ABORTED"
            echo "Environment: ${ENVIRONMENT}"
        }

        always {
            sh '''
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
