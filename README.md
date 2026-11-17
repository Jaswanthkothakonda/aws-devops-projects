# AWS & DevOps Engineering Portfolio

**Hands-on AWS Cloud | DevOps Automation | CI/CD | Infrastructure as Code | Containerization | Monitoring**

A practical collection of AWS Cloud and DevOps engineering projects, automation scripts, infrastructure configurations, and application deployment implementations.

This repository demonstrates hands-on experience in building CI/CD pipelines, containerizing applications, automating infrastructure, managing cloud deployments, and implementing application quality and reliability practices.

---

## About This Repository

This repository documents my practical learning and implementation of AWS Cloud and DevOps engineering concepts.

The projects are organized into six technical domains, covering individual tool-based implementations as well as an end-to-end application deployment project.

The primary objective is to demonstrate how different DevOps tools integrate into a practical software delivery workflow.

## Repository Structure

```text
aws-devops-projects/
│
├── CI-CD-Automation/
│   ├── Jenkinsfile
│   ├── Maven/
│   └── Linux/
│
├── AWS-Cloud-Infrastructure/
│   └── README.md
├── Containerization-Orchestration/
│   └── Docker/
│
├── Infrastructure-as-Code/
│   ├── Ansible/
│   └── Terraform/
│
├── Monitoring-Logging/
│   └── README.md
├── BeastEats-Project/
│   ├── app/
│   ├── tests/
│   ├── migrations/
│   ├── helm/
│   ├── Dockerfile
│   ├── Kubernetes manifests
│   └── sonar-project.properties
│
├── README.md
└── .gitignore
```

---

# Project Domains

## 1. CI/CD Automation

**Directory:** `CI-CD-Automation/`

Practical implementations of continuous integration, build automation, pipeline development, and Linux administration.

### Jenkins
- Developed a declarative Jenkins pipeline using a `Jenkinsfile`.
- Integrated a private GitHub repository with Jenkins using SSH credentials.
- Implemented automated checkout, workspace cleanup, and build information generation.
- Integrated Ansible syntax and inventory validation.
- Automated Docker image building and application testing.
- Integrated SonarCloud analysis and Quality Gate enforcement.
- Published automated test reports and coverage artifacts.
- Implemented Amazon ECR authentication, image publishing, and verification.
- Added production deployment approval and AWS Systems Manager-based deployment.
- Implemented application health checks and rollback handling.

### Maven
- Created a standalone Java Maven demonstration project.
- Organized application source code and unit tests using the Maven project structure.
- Configured dependencies and build lifecycle through `pom.xml`.
- Practiced Maven build and test integration with Jenkins.

### Linux & Bash Scripting
- Developed shell scripts for system and server administration.
- Implemented file and directory checks, loops, functions, and command-line arguments.
- Practiced error handling and safe scripting.
- Created disk usage and server health-check scripts.
- Implemented Docker and Git status-check scripts.

**Technologies:** Jenkins, Maven, Git, GitHub, Linux, Bash, Groovy.

## 2. AWS Cloud Infrastructure

**Directory:** `AWS-Cloud-Infrastructure/`

Reserved for organizing AWS service implementations, cloud architecture exercises, networking, storage, security, and deployment practicals.

The AWS services explored across my practical learning include:

- Amazon EC2 and EBS
- Amazon S3 and CloudFront
- Amazon VPC, subnets, and security groups
- Application Load Balancer
- Amazon RDS
- Amazon Route 53
- Amazon ECR
- Amazon ECS concepts
- Amazon CloudWatch
- AWS CloudTrail
- AWS Systems Manager
- AWS IAM
- Amazon EventBridge

The BeastEats project demonstrates selected AWS services integrated into an application deployment workflow.

## 3. Containerization & Orchestration

**Directory:** `Containerization-Orchestration/`

Practical containerization exercises focused on building, running, managing, and securing containerized applications.

### Docker
- Created Dockerfiles for application containerization.
- Practiced Docker image creation and container lifecycle management.
- Implemented Docker Compose configurations for multi-container applications.
- Explored Docker build optimization and security practices.
- Practiced container configuration and application port mapping.
- Docker image vulnerability scanning with Docker Scout is planned for a future practical.

### Orchestration
Kubernetes manifests and Helm deployment configurations are maintained within the BeastEats project.

**Technologies:** Docker, Docker Compose, Kubernetes, Helm, Amazon ECR.

## 4. Infrastructure as Code

**Directory:** `Infrastructure-as-Code/`

Infrastructure provisioning and configuration-management implementations using Terraform and Ansible.

### Terraform
- Organized infrastructure configurations into reusable `.tf` files.
- Created configurations for compute, storage, networking, and load balancing.
- Implemented security-related infrastructure configurations.
- Organized development environment configurations separately.
- Used Terraform variables, outputs, provider/version constraints, and dependency locking.
- Practiced infrastructure provisioning and management through Infrastructure as Code.

### Ansible
- Configured Ansible using `ansible.cfg`.
- Organized inventory and shared variables.
- Developed playbooks for automated server configuration.
- Implemented reusable roles for:
  - Common system configuration.
  - Docker service status and version checks.
  - BeastEats container checks, health validation, and environment-file configuration.
- Used Jinja2 templates for application environment configuration.
- Integrated Ansible syntax and inventory validation into the Jenkins pipeline.

**Technologies:** Terraform, Ansible, HCL, YAML, Jinja2.

## 5. Monitoring & Logging

**Directory:** `Monitoring-Logging/`

Dedicated category for monitoring, metrics collection, visualization, and centralized logging implementations.

Technologies planned for this section:

- Prometheus – Metrics collection and monitoring.
- Grafana – Metrics visualization and dashboards.
- Grafana Alloy – Telemetry and log collection.
- Loki – Centralized log storage and querying.

Monitoring and centralized logging integrations are planned for a future iteration.

## 6. BeastEats – End-to-End AWS & DevOps Project

**Directory:** `BeastEats-Project/`

BeastEats is a Python Flask-based food-ordering web application used to demonstrate the integration of application development, containerization, CI/CD automation, AWS deployment, configuration management, and orchestration.

### Application Development
- Developed a Flask-based web application.
- Organized application components into routes, models, authentication, templates, static CSS, and JavaScript.
- Configured database migration support.
- Implemented application health-check functionality.
- Created automated application tests using Pytest.

### Docker & Container Security
- Created a Dockerfile using Python 3.12 Slim as the base image.
- Configured Gunicorn to serve the Flask application.
- Configured the application to run using a non-root container user.
- Exposed application port 8000.
- Used Docker image tagging for build identification and deployment.

### CI/CD Pipeline Architecture

The Jenkins pipeline automates the application delivery process.

```text
GitHub Repository
       |
       v
Jenkins CI/CD Pipeline
       |
       +--> Git Checkout
       |
       +--> Ansible Validation
       |
       +--> Project Validation
       |
       +--> Docker Build
       |
       +--> Pytest & Coverage
       |
       +--> Publish Test Reports
       |
       +--> SonarCloud Analysis
       |
       +--> Quality Gate
       |
       +--> Amazon ECR Login
       |
       +--> Push & Verify Image
       |
       +--> Production Approval
       |
       v
AWS Systems Manager
       |
       v
Amazon EC2
       |
       v
Docker Container
       |
       v
BeastEats Application
```

### Automated Testing & Code Quality
- Integrated Pytest into the Jenkins pipeline.
- Generated JUnit XML test reports.
- Generated code coverage reports using `pytest-cov`.
- Published test results and coverage artifacts through Jenkins.
- Integrated SonarCloud for static code analysis.
- Configured Quality Gate enforcement to block further pipeline execution when the gate fails.

### Amazon ECR Integration
- Configured Amazon ECR as the private Docker image registry.
- Authenticated using AWS IAM-based permissions.
- Published uniquely tagged Docker images.
- Verified published images through AWS CLI.

### AWS Deployment
- Used an existing Amazon EC2 instance to host the application container.
- Integrated AWS Systems Manager Run Command into the Jenkins deployment workflow.
- Used IAM instance roles for AWS authentication.
- Pulled application images from Amazon ECR on the target EC2 instance.
- Configured persistent application storage and environment-file usage.
- Implemented application health validation after deployment.
- Added rollback handling to restore the previous container image when a new deployment fails.

### Kubernetes & Helm
- Created Kubernetes deployment, service, ingress, and persistent-volume-claim manifests.
- Organized Kubernetes application configurations using Helm.
- Created separate Helm values configurations for development and production.
- Practiced application deployment configuration and orchestration.

### Configuration Management
- Used Ansible to automate application server configuration.
- Organized playbooks, inventories, variables, and reusable roles.
- Integrated Ansible validation into the Jenkins pipeline.

### Monitoring & Logging
Monitoring and centralized logging integrations using Prometheus, Grafana, Grafana Alloy, and Loki are planned for a future iteration.

---

# Technology Stack

| Domain | Tools & Technologies |
|---|---|
| Cloud | AWS |
| Version Control | Git, GitHub |
| CI/CD | Jenkins |
| Programming | Python, Java |
| Scripting | Bash, Groovy |
| Build Automation | Maven |
| Containerization | Docker, Docker Compose |
| Orchestration | Kubernetes, Helm |
| Container Registry | Amazon ECR |
| Infrastructure as Code | Terraform |
| Configuration Management | Ansible |
| Code Quality | SonarCloud |
| Testing | Pytest, pytest-cov |
| Deployment | Amazon EC2, AWS Systems Manager |
| Monitoring | Prometheus, Grafana |
| Logging | Grafana Alloy, Loki |

---

# Engineering Practices

The projects in this repository demonstrate practical implementation of:

- CI/CD pipeline automation.
- Infrastructure provisioning and configuration management.
- Containerization and image management.
- Automated testing and code quality enforcement.
- AWS IAM-based authentication and access control.
- Application deployment and health validation.
- Deployment rollback and failure handling.
- Environment-specific configuration.
- Git version control and project documentation.

---

# About Me

I am an aspiring **AWS DevOps Engineer** with hands-on experience in AWS cloud services, Linux, Git, Jenkins, Docker, Kubernetes, Terraform, Ansible, and CI/CD automation.

I focus on building practical projects that demonstrate how cloud infrastructure, automation tools, and application delivery workflows work together.

**GitHub:** [Jaswanthkothakonda](https://github.com/Jaswanthkothakonda)

---

*Learning, building, automating, and improving through practical AWS Cloud and DevOps engineering projects.*