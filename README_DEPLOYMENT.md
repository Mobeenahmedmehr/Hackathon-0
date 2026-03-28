# Deployment Guide for AI Employee System

This guide provides comprehensive instructions for deploying the AI Employee system in various environments.

## Table of Contents
- [Local Setup Instructions](#local-setup-instructions)
- [Environment Variable Setup](#environment-variable-setup)
- [Running with Python](#running-with-python)
- [Running with Docker](#running-with-docker)
- [Deploying on VPS (Ubuntu)](#deploying-on-vps-ubuntu)
- [Troubleshooting Common Errors](#troubleshooting-common-errors)

## Local Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Git
- Pip package manager
- Playwright-compatible browser environment

### Installing Dependencies

Before running the system, you need to install all required dependencies:

```bash
pip install -r requirements.txt
```

For convenience, we provide automated scripts to set up your environment:

**On Unix/Linux/Mac:**
```bash
bash scripts/install_dependencies.sh
```

**On Windows:**
```cmd
scripts\install_dependencies.bat
```

These scripts will:
- Create a virtual environment
- Activate the environment
- Install all required packages from requirements.txt
- Install Playwright browsers (chromium, firefox, webkit)

After installation, you can validate that all dependencies are correctly installed:
```bash
python scripts/validate_setup.py
```

### Installation Steps

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-directory>
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Run the setup script:
```bash
bash scripts/setup.sh
```

## Environment Variable Setup

The system requires several environment variables to function properly. Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

### Required Variables

- `GOOGLE_APPLICATION_CREDENTIALS`: Path to your Google service account JSON file
- `GMAIL_CLIENT_ID`: Your Gmail OAuth client ID
- `GMAIL_CLIENT_SECRET`: Your Gmail OAuth client secret
- `GMAIL_REDIRECT_URI`: Redirect URI for Gmail OAuth
- `WHATSAPP_TOKEN`: Your WhatsApp business API token
- `LINKEDIN_CLIENT_ID`: Your LinkedIn OAuth client ID
- `LINKEDIN_CLIENT_SECRET`: Your LinkedIn OAuth client secret

### Optional Variables

- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR) - defaults to INFO
- `WATCHER_POLL_INTERVAL`: Polling interval for watchers in seconds - defaults to 30
- `MAX_RETRIES`: Maximum number of retries for failed operations - defaults to 3

## Running with Python

### Direct Python Execution

1. Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
playwright install chromium
```

2. Run the system:
```bash
python run_system.py
```

### Using the Start Script

Alternatively, use the provided start script:
```bash
bash scripts/start.sh
```

## Running with Docker

### Building and Running

1. Build and run with Docker Compose (recommended):
```bash
docker-compose up --build
```

2. Or build and run manually:
```bash
# Build the image
docker build -t ai-employee-system .

# Run the container
docker run -d --env-file .env --name ai-employee-container ai-employee-system
```

### Docker Compose Configuration

The `docker-compose.yml` file defines the following services:
- `ai_employee_app`: Main application service with auto-restart enabled
- Volume mappings for data persistence
- Environment variable loading from `.env` file

### Managing Docker Containers

```bash
# View running containers
docker-compose ps

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Restart services
docker-compose restart
```

## Deploying on VPS (Ubuntu)

### Initial Server Setup

1. Update system packages:
```bash
sudo apt update && sudo apt upgrade -y
```

2. Install prerequisites:
```bash
sudo apt install -y python3 python3-pip python3-venv git nodejs npm
```

3. Install Docker:
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

4. Log out and log back in to apply Docker group changes:
```bash
exit
# Log back in
```

### Deploy the Application

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-directory>
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your credentials
nano .env
```

3. Make scripts executable:
```bash
chmod +x scripts/setup.sh scripts/start.sh
```

4. Run setup:
```bash
bash scripts/setup.sh
```

5. Run the application with systemd (recommended for production):

Create a systemd service file:
```bash
sudo nano /etc/systemd/system/ai-employee.service
```

Add the following content (adjust paths as needed):
```ini
[Unit]
Description=AI Employee System
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/home/your_username/path/to/ai-employee
ExecStart=/usr/bin/python3 /home/your_username/path/to/ai-employee/run_system.py
Restart=always
RestartSec=10

Environment=PYTHONPATH=/home/your_username/path/to/ai-employee
EnvironmentFile=/home/your_username/path/to/ai-employee/.env

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable ai-employee
sudo systemctl start ai-employee
```

Check the status:
```bash
sudo systemctl status ai-employee
```

View logs:
```bash
sudo journalctl -u ai-employee -f
```

### Reverse Proxy with Nginx (Optional)

If you need to expose a web interface, install and configure Nginx:

```bash
sudo apt install nginx
sudo nano /etc/nginx/sites-available/ai-employee
```

Add configuration:
```
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;  # Adjust port if needed
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/ai-employee /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Troubleshooting Common Errors

### Common Issues and Solutions

#### 1. Module Import Errors
**Problem**: `ModuleNotFoundError` for various packages
**Solution**:
```bash
pip install -r requirements.txt
# Or if using virtual environment:
source venv/bin/activate
pip install -r requirements.txt
```

#### 2. Playwright Browser Issues
**Problem**: Playwright unable to find browser
**Solution**:
```bash
playwright install chromium
# Or for all browsers:
playwright install
```

#### 3. Permission Errors
**Problem**: Permission denied when accessing files
**Solution**: Check file permissions and ensure the running user has access:
```bash
chmod +x scripts/*.sh
chown -R $USER:$USER /path/to/project
```

#### 4. Environment Variables Not Loading
**Problem**: Application fails due to missing environment variables
**Solution**: Verify `.env` file exists and has correct format:
- No spaces around `=` in variable assignments
- Values with spaces should be quoted
- File should be in the correct directory

#### 5. Docker Build Failures
**Problem**: Docker build fails with dependency errors
**Solution**:
- Clear Docker cache: `docker system prune -a`
- Ensure Dockerfile has correct paths
- Check that all required files exist

#### 6. Gmail API Authentication Issues
**Problem**: Gmail authentication fails
**Solution**:
- Verify credentials in `.env` file
- Ensure Google Cloud project has Gmail API enabled
- Check that credentials file path is correct
- Verify OAuth consent and scopes

#### 7. Memory Issues
**Problem**: Application crashes due to high memory usage
**Solution**:
- Monitor memory usage: `htop` or `top`
- Consider increasing swap space on VPS
- Optimize code for memory usage
- Restart service if needed: `systemctl restart ai-employee`

#### 8. Process Not Starting
**Problem**: Application doesn't start or dies immediately
**Solution**:
- Check logs for error messages
- Verify all required dependencies are installed
- Ensure environment variables are properly set
- Check file permissions

### Debugging Tips

1. **Check logs first**: Look at the application logs in the `Logs/` directory
2. **Verify environment**: Ensure all environment variables are set correctly
3. **Test connectivity**: Verify network connectivity to external services
4. **Resource monitoring**: Monitor CPU and memory usage
5. **Dependency check**: Confirm all required packages are installed

### Support Commands

Useful commands for troubleshooting:

```bash
# Check running processes
ps aux | grep python

# Check disk space
df -h

# Check memory usage
free -h

# Check system logs
journalctl -u ai-employee

# View application logs
tail -f Logs/*.log
```

### Getting Help

If issues persist:
1. Check the application logs in the `Logs/` directory
2. Verify all prerequisites are met
3. Review the `.env` file for any misconfigurations
4. Consult the system documentation
5. Reach out to the development team with detailed error information