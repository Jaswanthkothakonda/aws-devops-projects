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

        choice(
            name: 'DEPLOY_TO_EC2',
            choices: ['no', 'yes'],
            description: 'Enable SSM deployment. Keep no for validation-only builds.'
        )
    }

    environment {
        AWS_REGION = 'ap-south-2'
        ECR_REGISTRY = '734648185802.dkr.ecr.ap-south-2.amazonaws.com'
        ECR_REPOSITORY = 'beasteats'
        IMAGE_TAG = "${BUILD_NUMBER}"

        SSM_TARGET_INSTANCE_ID = 'i-01e6876866d6bb05c'
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
                    checkout([
                        $class: 'GitSCM',
                        branches: [[name: '*/main']],
                        userRemoteConfigs: [[
                            url: 'git@github.com:Jaswanthkothakonda/aws-devops-projects.git',
                            credentialsId: 'github-jenkins-ssh'
                        ]]
                    ])
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

                    env.UNIQUE_IMAGE_TAG =
                        "jenkins-${BUILD_NUMBER}-${env.GIT_COMMIT_SHORT}"

                    env.IMAGE_URI =
                        "${ECR_REGISTRY}/${ECR_REPOSITORY}:${env.UNIQUE_IMAGE_TAG}"
                }

                sh '''
                    echo "===== BeastEats CI/CD Pipeline ====="
                    echo "Build: ${BUILD_NUMBER}"
                    echo "Environment: ${ENVIRONMENT}"
                    echo "Commit: ${GIT_COMMIT_SHORT}"
                    echo "Unique image tag: ${UNIQUE_IMAGE_TAG}"
                '''
            }
        }

        stage('Validate BeastEats Project') {
            steps {
                sh '''
                    set -eu

                    test -f BeastEats/Dockerfile
                    test -f BeastEats/requirements.txt
                    test -f BeastEats/app/__init__.py
                    test -f BeastEats/tests/test_app.py
                    test -f sonar-project.properties

                    docker --version
                    aws --version

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
Image Tag: ${UNIQUE_IMAGE_TAG}
Image URI: ${IMAGE_URI}
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
                echo "Deployment enabled: ${DEPLOY_TO_EC2}"
            }
        }

        stage('Docker Build') {
            steps {
                sh '''
                    set -eu

                    docker build \
                        -t ${ECR_REPOSITORY}:${IMAGE_TAG} \
                        -t ${ECR_REPOSITORY}:${IMAGE_TAG}-${GIT_COMMIT_SHORT} \
                        -t ${ECR_REPOSITORY}:${UNIQUE_IMAGE_TAG} \
                        -t ${IMAGE_URI} \
                        BeastEats
                '''
            }
        }

        stage('BeastEats Automated Tests') {
            steps {
                sh '''
                    set -eu

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
                        withEnv([
                            'SONAR_SCANNER_JAVA_OPTS=-Xmx384m -XX:ActiveProcessorCount=1'
                        ]) {
                            sh """
                                ${scannerHome}/bin/sonar-scanner \
                                    -Dproject.settings=sonar-project.properties
                            """
                        }
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
                        set -eu

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
                    set -eu

                    echo "Publishing unique image tag: ${IMAGE_URI}"

                    docker push "${IMAGE_URI}"

                    echo "Successfully pushed ${IMAGE_URI}"
                '''
            }
        }

        stage('Verify ECR') {
            steps {
                sh '''
                    set -eu

                    aws ecr describe-images \
                        --repository-name "${ECR_REPOSITORY}" \
                        --image-ids imageTag="${UNIQUE_IMAGE_TAG}" \
                        --region "${AWS_REGION}"

                    echo "ECR image verified: ${IMAGE_URI}"
                '''
            }
        }

        stage('Production Approval') {
            when {
                allOf {
                    environment name: 'ENVIRONMENT', value: 'production'
                    expression { params.DEPLOY_TO_EC2 == 'yes' }
                }
            }

            steps {
                input(
                    message: "Approve BeastEats production release of ${env.UNIQUE_IMAGE_TAG}?",
                    ok: 'Approve Release'
                )
            }
        }

        stage('Deploy to EC2 via SSM') {
            when {
                expression { params.DEPLOY_TO_EC2 == 'yes' }
            }

            steps {
                script {
                    withEnv([
                        "DEPLOY_IMAGE_URI=${env.IMAGE_URI}",
                        "DEPLOY_REGION=${env.AWS_REGION}",
                        "DEPLOY_INSTANCE=${env.SSM_TARGET_INSTANCE_ID}"
                    ]) {
                        sh '''
                            set -eu

                            TMP_DIR=$(mktemp -d)
                            trap 'rm -rf "$TMP_DIR"' EXIT

                            export DEPLOY_IMAGE_URI
                            export DEPLOY_REGION

                            python3 - "$TMP_DIR/ssm-parameters.json" <<'PY'
import json
import os
import shlex
import sys

image_uri = os.environ["DEPLOY_IMAGE_URI"]
region = os.environ["DEPLOY_REGION"]

commands = [
    "set -eu",
    "test -f /opt/beasteats/.env",
    "mountpoint -q /app/instance",
    "docker inspect beasteats-app >/dev/null",
    f"IMAGE_URI={shlex.quote(image_uri)}",
    f"REGION={shlex.quote(region)}",
    'aws ecr get-login-password --region "$REGION" | docker login --username AWS --password-stdin 734648185802.dkr.ecr.ap-south-2.amazonaws.com',
    'docker pull "$IMAGE_URI"',
    'OLD_IMAGE_ID=$(docker inspect --format "{{.Image}}" beasteats-app)',
    'echo "Previous image ID: $OLD_IMAGE_ID"',
    'docker stop beasteats-app',
    'docker rm beasteats-app',
    'if docker run -d --name beasteats-app --restart unless-stopped -p 8000:8000 --env-file /opt/beasteats/.env -v /app/instance:/app/instance "$IMAGE_URI"; then echo "New container started"; else echo "New container failed to start"; fi',
    'sleep 10',
    'if curl -fsS http://127.0.0.1:8000/health; then echo "BeastEats deployment health check passed"; else echo "Health check failed; rolling back"; docker logs --tail 100 beasteats-app || true; docker rm -f beasteats-app || true; docker run -d --name beasteats-app --restart unless-stopped -p 8000:8000 --env-file /opt/beasteats/.env -v /app/instance:/app/instance "$OLD_IMAGE_ID"; sleep 5; curl -fsS http://127.0.0.1:8000/health || true; exit 1; fi'
]

with open(sys.argv[1], "w") as f:
    json.dump({"commands": commands}, f)
PY

                            COMMAND_ID=$(aws ssm send-command \
                                --instance-ids "$DEPLOY_INSTANCE" \
                                --document-name "AWS-RunShellScript" \
                                --parameters "file://$TMP_DIR/ssm-parameters.json" \
                                --comment "BeastEats deployment ${BUILD_NUMBER}" \
                                --region "$DEPLOY_REGION" \
                                --query 'Command.CommandId' \
                                --output text)

                            echo "SSM Command ID: $COMMAND_ID"

                            STATUS="Pending"
                            ATTEMPTS=0

                            while [ "$ATTEMPTS" -lt 60 ]; do
                                STATUS=$(aws ssm get-command-invocation \
                                    --command-id "$COMMAND_ID" \
                                    --instance-id "$DEPLOY_INSTANCE" \
                                    --region "$DEPLOY_REGION" \
                                    --query 'Status' \
                                    --output text 2>/dev/null || echo "Pending")

                                echo "Deployment status: $STATUS"

                                case "$STATUS" in
                                    Success)
                                        break
                                        ;;
                                    Failed|Cancelled|TimedOut|Cancelling)
                                        aws ssm get-command-invocation \
                                            --command-id "$COMMAND_ID" \
                                            --instance-id "$DEPLOY_INSTANCE" \
                                            --region "$DEPLOY_REGION" \
                                            --query '[Status,StandardOutputContent,StandardErrorContent]' \
                                            --output json || true
                                        exit 1
                                        ;;
                                esac

                                ATTEMPTS=$((ATTEMPTS + 1))
                                sleep 5
                            done

                            if [ "$STATUS" != "Success" ]; then
                                echo "SSM deployment did not complete successfully."
                                exit 1
                            fi

                            aws ssm get-command-invocation \
                                --command-id "$COMMAND_ID" \
                                --instance-id "$DEPLOY_INSTANCE" \
                                --region "$DEPLOY_REGION" \
                                --query '[Status,StandardOutputContent,StandardErrorContent]' \
                                --output json
                        '''
                    }
                }
            }
        }
    }

    post {
        success {
            echo "BEASTEATS PIPELINE SUCCESS"
            echo "Environment: ${ENVIRONMENT}"
            echo "Unique image tag: ${env.UNIQUE_IMAGE_TAG}"
            echo "Image URI: ${env.IMAGE_URI}"
            echo "EC2 deployment requested: ${DEPLOY_TO_EC2}"

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
                    "${ECR_REPOSITORY}:${IMAGE_TAG}" \
                    "${ECR_REPOSITORY}:${IMAGE_TAG}-${GIT_COMMIT_SHORT}" \
                    "${ECR_REPOSITORY}:${UNIQUE_IMAGE_TAG}" \
                    "${IMAGE_URI}" \
                    2>/dev/null || true
            '''
        }
    }
}
