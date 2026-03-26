# Two-Tier Flask App with CI/CD Pipeline

A simple message board web application built with Flask and MySQL, 
deployed automatically using Jenkins, Docker, and Docker Compose on AWS EC2.

---

## What This Project Does

- Users can type a message on a web page and submit it
- The message gets saved to a MySQL database
- All messages are displayed on the same page
- Every time new code is pushed to GitHub, Jenkins automatically 
  builds and deploys the updated app — no manual work needed

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python / Flask | Web application |
| MySQL | Database |
| Docker | Containerisation |
| Docker Compose | Running multiple containers together |
| Jenkins | CI/CD pipeline automation |
| AWS EC2 | Cloud server |
| GitHub | Source code management |

---

## Project Structure
```
two-tier-flask-app/
├── templates/
│   └── index.html        # Frontend HTML page
├── app.py                # Flask application
├── Dockerfile            # Instructions to build Flask container
├── docker-compose.yml    # Runs Flask + MySQL containers together
├── Jenkinsfile           # CI/CD pipeline definition
├── message.sql           # Database and table setup
└── requirements.txt      # Python dependencies
```

---

## How It Works
```
Developer pushes code to GitHub
            ↓
Jenkins detects the push
            ↓
Jenkins pulls latest code from GitHub
            ↓
Jenkins builds Docker image for Flask app
            ↓
Jenkins runs Docker Compose (starts Flask + MySQL)
            ↓
Jenkins checks app is healthy
            ↓
App is live at http://<EC2-IP>:5000
```

---

## How to Run This Project

### Prerequisites
- An AWS account
- A GitHub account
- Basic knowledge of terminal/command line

---

### Step 1 — Launch AWS EC2 Instance

1. Go to AWS Console → EC2 → Launch Instance
2. Choose **Ubuntu 22.04 LTS**
3. Choose **t2.micro** (free tier)
4. Create a key pair and download the `.pem` file
5. Add these inbound rules in Security Group:

| Port | Purpose |
|------|---------|
| 22 | SSH access |
| 80 | HTTP |
| 5000 | Flask app |
| 8080 | Jenkins |

6. Launch the instance

---

### Step 2 — Connect to EC2
```bash
chmod 400 /path/to/your-key.pem
ssh -i /path/to/your-key.pem ubuntu@<YOUR-EC2-PUBLIC-IP>
```

---

### Step 3 — Install Docker and Git
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install git docker.io docker-compose-v2 -y
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER
newgrp docker
```

---

### Step 4 — Install Java
```bash
sudo apt install openjdk-17-jdk -y
```

---

### Step 5 — Install Jenkins
```bash
curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key | sudo tee \
  /usr/share/keyrings/jenkins-keyring.asc > /dev/null

echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
  https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null

sudo apt update
sudo apt install jenkins -y
sudo systemctl start jenkins
sudo systemctl enable jenkins
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
```

---

### Step 6 — Open Jenkins

1. Go to `http://<YOUR-EC2-PUBLIC-IP>:8080`
2. Get the initial password:
```bash
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```
3. Paste it in Jenkins, install suggested plugins, create admin user

---

### Step 7 — Create Jenkins Pipeline

1. Jenkins dashboard → **New Item**
2. Name it `two-tier-flask-app`, choose **Pipeline**, click **OK**
3. Scroll to **Pipeline** section
4. Set Definition to **Pipeline script from SCM**
5. Choose **Git**
6. Enter your GitHub repository URL
7. Set Script Path to `Jenkinsfile`
8. Click **Save**

---

### Step 8 — Run the Pipeline

1. Click **Build Now**
2. Watch the stages run in **Stage View**
3. Once successful, visit `http://<YOUR-EC2-PUBLIC-IP>:5000`

---

## CI/CD Flow Explained

### What happens on every git push:
1. **Clone Code** — Jenkins pulls latest code from GitHub
2. **Build Docker Image** — builds the Flask container
3. **Deploy** — stops old containers, starts new ones
4. **Health Check** — confirms app is running at `/health`
5. **Report** — Jenkins reports success or failure

---

## Key Concepts Learned

- **Dockerfile** — recipe for building a single container
- **Docker Compose** — runs multiple containers together
- **Jenkins Pipeline** — automates build and deploy on every push
- **Health checks** — confirms app is running after deployment
- **Environment variables** — keeps credentials out of code

---