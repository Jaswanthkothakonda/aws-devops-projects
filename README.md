# BeastEats – AWS Cloud & DevOps Project

**A Flask-based food ordering application deployed using AWS cloud services and an automated DevOps workflow.**

## Overview

BeastEats is a food ordering web application built with Python and Flask. This project demonstrates the practical implementation of containerization, CI/CD automation, cloud deployment, security, monitoring, and automated testing using AWS and DevOps tools.

## Architecture

```text
GitHub
  |
  v
Jenkins CI/CD
  |
  +---- Docker Build
  |
  +---- Pytest
  |
  +---- SonarCloud Analysis
  |
  +---- Quality Gate
  |
  v
Amazon ECR
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

## Technology Stack

| Category | Technologies |
|---|---|
| Application | Python, Flask |
| Cloud | AWS |
| CI/CD | Jenkins, GitHub |
| Containers | Docker |
| Container Registry | Amazon ECR |
| Deployment | Amazon EC2, AWS Systems Manager |
| Code Quality | SonarCloud |
| Testing | Pytest, pytest-cov |
| Infrastructure as Code | Terraform |
| Configuration Management | Ansible |
| Monitoring | Prometheus, Grafana |
| Logging | Grafana Alloy, Loki |
| Other Tools | Linux, Bash, Maven, Kubernetes, Helm |

## Key Implementations

**1. Application and Containerization**
- Developed a Flask-based food ordering application.
- Created Docker images using Python 3.12 and Gunicorn.
- Configured a non-root application user and container port 8000.

**2. CI/CD Automation**
- Integrated GitHub with Jenkins using a Jenkinsfile.
- Automated project validation, Docker builds, and application tests.
- Integrated SonarCloud analysis and Quality Gate enforcement.
- Published test reports and coverage artifacts.
- Automated image publishing to Amazon ECR.

**3. AWS Cloud Deployment**
- Deployed the application on an existing Amazon EC2 instance.
- Used Amazon ECR for container image storage.
- Automated deployment through AWS Systems Manager.
- Used IAM roles and security groups to control access.
- Configured application health validation.

**4. Security and Infrastructure**
- Implemented IAM permissions and least-privilege access.
- Implemented ECR image scanning and lifecycle policies.
- Used Terraform for AWS infrastructure automation.
- Worked with Ansible for configuration-management automation.

**5. Monitoring and Logging**
- Used Prometheus and Grafana for monitoring.
- Used Grafana Alloy to collect container logs.
- Used Loki for centralized log querying.

## Testing and Validation

The application test suite covers health checks, homepage responses, menu and category APIs, user registration, and authentication.

<badge color="success">11 tests passed</badge>

Verified using Docker with Python 3.12.16 and pytest 9.2.0.

Application health endpoint:

```bash
curl http://localhost:8000/health
```

Verified response:

```json
{
  "application": "BeastEats",
  "status": "healthy",
  "version": "1.0.0"
}
```

## Repository Structure

```text
aws-devops-projects/
├── BeastEats/
│   ├── app/
│   ├── tests/
│   ├── migrations/
│   ├── helm/
│   ├── Dockerfile
│   └── requirements.txt
├── ansible/
├── docker/
├── linux/
├── maven-demo/
├── terraform/
├── Jenkinsfile
├── README.md
└── .gitignore
```

## Project Highlights

- Automated CI/CD pipeline using Jenkins.
- Docker image management with Amazon ECR.
- AWS EC2 deployment through Systems Manager.
- SonarCloud quality analysis and automated testing.
- AWS security and infrastructure automation.
- Monitoring and centralized container logging.

## About Me

Aspiring **AWS DevOps Engineer** with hands-on experience in AWS cloud services, CI/CD, Docker, Jenkins, Terraform, Ansible, Kubernetes, and monitoring tools.

**GitHub:** [Jaswanthkothakonda](https://github.com/Jaswanthkothakonda)

---

*Building and deploying applications through AWS Cloud and DevOps automation.*
