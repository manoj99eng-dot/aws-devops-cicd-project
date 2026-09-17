# AWS DevOps CI/CD Project

An end-to-end **CI/CD pipeline** for deploying a Python Flask application to **AWS EC2** using **GitHub, Jenkins, Docker, and Docker Hub**.

The pipeline is triggered automatically whenever new code is pushed to the `main` branch. Jenkins checks out the source code, tests the application, builds a Docker image, pushes the image to Docker Hub, deploys the new container on AWS EC2, and performs a health check.

---

## 🚀 Project Overview

This project demonstrates a complete DevOps workflow:

```text
Developer
    │
    │ git push
    ▼
GitHub Repository
    │
    │ GitHub Webhook
    ▼
Jenkins
    │
    ├── Checkout Source Code
    ├── Run Tests
    ├── Build Docker Image
    ├── Login to Docker Hub
    ├── Push Docker Image
    └── Deploy Container
             │
             ▼
        AWS EC2
             │
             ▼
      Flask Application
             │
             ▼
        Health Check
```

---

## 🛠️ Technologies Used

| Technology          | Purpose                       |
| ------------------- | ----------------------------- |
| **AWS EC2**         | Application hosting           |
| **Jenkins**         | CI/CD automation              |
| **GitHub**          | Source code management        |
| **GitHub Webhooks** | Automatic pipeline triggering |
| **Docker**          | Application containerization  |
| **Docker Hub**      | Container image registry      |
| **Python**          | Application development       |
| **Flask**           | Web application framework     |
| **Linux**           | Server operating system       |
| **Git**             | Version control               |

---

## 📁 Project Structure

```text
aws-devops-cicd-project/
│
├── app/
│   ├── app.py
│   └── requirements.txt
│
├── Dockerfile
├── Jenkinsfile
└── README.md
```

### File Description

#### `app/app.py`

Contains the Flask web application.

The application provides:

* `/` — Main application page
* `/health` — Application health endpoint

#### `app/requirements.txt`

Contains the Python dependencies required by the Flask application.

#### `Dockerfile`

Defines the Docker image used to package the Flask application.

#### `Jenkinsfile`

Defines the complete Jenkins CI/CD pipeline.

#### `README.md`

Project documentation.

---

# 🔄 CI/CD Pipeline

The Jenkins pipeline contains the following stages.

## 1. Checkout

Jenkins retrieves the latest source code from the GitHub `main` branch.

```text
GitHub → Jenkins
```

Repository:

```text
https://github.com/manoj99eng-dot/aws-devops-cicd-project.git
```

---

## 2. Test

The pipeline creates a Python virtual environment and installs application dependencies.

It then performs Python syntax validation using:

```bash
python -m py_compile app/app.py
```

This helps detect Python syntax errors before the Docker image is built.

---

## 3. Docker Build

Jenkins builds the application into a Docker image.

Images are tagged using the Jenkins build number:

```text
manoj99eng/aws-devops-app:<BUILD_NUMBER>
```

A `latest` image is also created:

```text
manoj99eng/aws-devops-app:latest
```

Example:

```text
manoj99eng/aws-devops-app:2
```

---

## 4. Docker Hub Login

Jenkins securely authenticates with Docker Hub using Jenkins credentials.

The Docker Hub credentials are stored in Jenkins rather than being hard-coded into the pipeline.

Credential ID:

```text
docker-hub-creds
```

---

## 5. Docker Push

Jenkins pushes the Docker images to Docker Hub.

```text
Jenkins
   │
   ├── Versioned Image
   │
   └── Latest Image
          │
          ▼
      Docker Hub
```

Docker Hub namespace:

```text
manoj99eng
```

---

## 6. Deploy to AWS EC2

The pipeline automatically:

1. Stops the previous application container.
2. Removes the previous container.
3. Pulls the newly built image.
4. Starts a new container.
5. Waits for the application to start.
6. Checks the container status.
7. Performs an application health check.

Container name:

```text
aws-devops-app
```

Application port:

```text
5000
```

Docker mapping:

```text
EC2:5000 → Container:5000
```

---

# 🔗 GitHub Webhook Automation

The project uses a **GitHub Webhook** to automatically trigger Jenkins.

The workflow is:

```text
Developer
   │
   │ git push
   ▼
GitHub
   │
   │ Webhook
   ▼
Jenkins
   │
   ▼
CI/CD Pipeline
   │
   ▼
Docker Build
   │
   ▼
Docker Hub
   │
   ▼
AWS EC2 Deployment
```

This eliminates the need to manually start a Jenkins build after every code change.

---

# 🐳 Docker Configuration

The application uses Python 3.12 with a slim Python base image.

Example Docker configuration:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

EXPOSE 5000

CMD ["python", "app.py"]
```

---

# ⚙️ Jenkins Pipeline

The pipeline is defined using a Jenkins Declarative Pipeline.

Main stages:

```text
Checkout
   ↓
Test
   ↓
Docker Build
   ↓
Docker Login
   ↓
Docker Push
   ↓
Deploy to EC2
```

The pipeline uses Jenkins environment variables for:

```text
IMAGE_NAME
LATEST_IMAGE
CONTAINER_NAME
APP_PORT
```

This makes the pipeline easier to maintain and modify.

---

# ☁️ AWS Infrastructure

The application is deployed on:

```text
AWS EC2
```

The EC2 server runs:

```text
Linux
Docker
Jenkins
```

The Flask application runs inside a Docker container.

Application architecture:

```text
Internet
   │
   │ HTTP :5000
   ▼
AWS EC2
   │
   ▼
Docker Container
   │
   ▼
Flask Application
```

---

# 🔐 Security

The project follows several basic DevOps security practices.

### Jenkins Credentials

Docker Hub credentials are stored in Jenkins Credentials instead of being placed directly inside the Jenkinsfile.

### Environment Variables

Sensitive authentication information is passed through Jenkins-managed credentials.

### Container Isolation

The Flask application runs inside a Docker container instead of directly on the host operating system.

### Security Groups

AWS EC2 Security Groups control inbound access to the server and application ports.

> For production environments, Jenkins should not be exposed broadly on port `8080`. HTTPS, restricted source IPs, authentication, and/or a reverse proxy should be used.

---

# 🧪 Application Health Check

The Flask application exposes:

```text
/health
```

Example response:

```json
{
  "status": "healthy"
}
```

Jenkins verifies the deployment using:

```bash
curl --fail http://localhost:5000/health
```

If the health check fails, the deployment stage fails.

---

# ▶️ Running the Application Locally

Clone the repository:

```bash
git clone https://github.com/manoj99eng-dot/aws-devops-cicd-project.git
```

Enter the project directory:

```bash
cd aws-devops-cicd-project
```

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate it:

### Linux/macOS

```bash
source venv/bin/activate
```

### Windows PowerShell

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r app/requirements.txt
```

Run the application:

```bash
python app/app.py
```

The application will be available at:

```text
http://localhost:5000
```

Health endpoint:

```text
http://localhost:5000/health
```

---

# 🐳 Running with Docker

Build the image:

```bash
docker build -t manoj99eng/aws-devops-app:latest .
```

Run the container:

```bash
docker run -d \
  --name aws-devops-app \
  -p 5000:5000 \
  manoj99eng/aws-devops-app:latest
```

Check the container:

```bash
docker ps
```

Test the application:

```bash
curl http://localhost:5000/health
```

Expected response:

```json
{
  "status": "healthy"
}
```

---

# 🔧 Jenkins Configuration

The Jenkins job is configured to use the GitHub repository:

```text
https://github.com/manoj99eng-dot/aws-devops-cicd-project.git
```

Branch:

```text
main
```

The Jenkins job uses the `Jenkinsfile` stored in the repository.

### Required Jenkins Credential

Create a Jenkins credential with:

```text
Credential ID: docker-hub-creds
```

The credential should contain the Docker Hub username and password/token.

---

# 📦 Docker Image

Docker Hub repository:

```text
manoj99eng/aws-devops-app
```

Images are tagged with Jenkins build numbers.

Example:

```text
manoj99eng/aws-devops-app:1
manoj99eng/aws-devops-app:2
manoj99eng/aws-devops-app:3
```

This provides a simple version history for deployed container images.

---

# 🔁 Deployment Strategy

The current deployment process uses a simple container replacement strategy.

```text
Old Container
     │
     ▼
docker stop
     │
     ▼
docker rm
     │
     ▼
docker pull
     │
     ▼
New Container
```

The new container is configured with:

```text
--restart unless-stopped
```

This allows Docker to automatically restart the application container if the Docker service or host restarts.

---

# 📊 DevOps Concepts Demonstrated

This project demonstrates practical experience with:

* Continuous Integration
* Continuous Deployment
* Git-based development workflow
* GitHub Webhooks
* Jenkins Declarative Pipelines
* Jenkins Credentials
* Docker image creation
* Docker image versioning
* Docker Hub
* Container deployment
* AWS EC2
* Linux server administration
* Application health checks
* Automated deployment validation
* Infrastructure access through AWS Security Groups

---

# 🎯 Project Objectives

The main objectives of this project are:

1. Automate application testing.
2. Automate Docker image creation.
3. Automate Docker image publishing.
4. Automate EC2 deployment.
5. Trigger deployments automatically from GitHub.
6. Verify application health after deployment.
7. Demonstrate a practical end-to-end DevOps workflow.

---

# 💼 Resume Description

### AWS DevOps CI/CD Pipeline

**Technologies:** AWS EC2, Jenkins, GitHub, GitHub Webhooks, Docker, Docker Hub, Python, Flask, Linux

> Developed an end-to-end CI/CD pipeline for a Python Flask application using GitHub, Jenkins, Docker and AWS EC2. Implemented GitHub webhook-triggered Jenkins builds, automated application testing, Docker image creation and versioning, Docker Hub publishing, automated EC2 container deployment, and post-deployment health validation.

---

# 📌 Key Achievement

The project implements the following automated workflow:

```text
git push
   ↓
GitHub Webhook
   ↓
Jenkins
   ↓
Code Checkout
   ↓
Application Test
   ↓
Docker Build
   ↓
Docker Hub Push
   ↓
EC2 Deployment
   ↓
Container Health Check
   ↓
Deployment Complete
```

This demonstrates an end-to-end automated DevOps delivery process from **source code commit to running application**.

---

# 👨‍💻 Author

**Manoj**

GitHub:

```text
https://github.com/manoj99eng-dot
```

Docker Hub:

```text
https://hub.docker.com/u/manoj99eng
```

---

# 📄 License

This project is intended for learning, portfolio development, and demonstration of DevOps CI/CD practices.
