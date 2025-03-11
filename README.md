# Django App for SBA Banking Loan Application 🚀

![Banking App](https://i.imgur.com/FVRBQAT.png)


## Overview

This project is a comprehensive web application developed with Django to facilitate SBA Loan Request. It provides a platform for businesses to:
- **Request Loans** via an intuitive form.
- Access secure **Client & Advisor Portals**.
- **Chat in Real-Time** with banking advisors.
- Stay up-to-date with the latest **Bank News**.

All while maintaining robust security measures such as CSRF/XSS protection and encrypted password storage.

## Objectives

- **Loan Requests:** Allow companies to apply for loans easily.
- **Role-Based Access:** Separate secure areas for clients and banking advisors.
- **Real-Time Communication:** Integrated chat using Django Channels (WebSockets).
- **News Management:** Create and publish bank news on the homepage.
- **Enhanced Security:** Secure authentication with encrypted passwords.

## Technologies Used

- **Language:** Python 🐍
- **Framework:** Django 🕸️
- **Database:** MSSQL (Azure) / PostgreSQL (Local) / SQLite (Local) 🗄️
- **Frontend:** HTML, CSS, JavaScript & Tailwind CSS 🎨
- **Real-Time:** Django Channels (WebSockets) 💬
- **Deployment:** Docker, Azure Container Instances & Terraform ☁️

## Features

- **User Authentication:** Secure signup and login with role restrictions.
- **Loan Management:** Submit, track, and manage loan requests.
- **Instant Messaging:** Real-time chat between clients and advisors.
- **News Publishing:** Dynamically post and manage bank news.
- **Admin Tools:** Dashboard for monitoring user activities and loan approvals.
- **Security:** CSRF/XSS protection and strong password hashing.

## Project Structure

```
MySbaApp/
├── Dockerfile                   # Docker configuration
├── docker-compose.yaml          # Docker Compose definitions
├── MySbaApp/                    # Django project root
│   ├── asgi.py                  # ASGI entry point (for WebSockets)
│   ├── settings.py              # Django settings
│   ├── urls.py                  # URL routing
│   └── wsgi.py                  # WSGI entry point
├── sbapp/                       # Main Django app
│   ├── forms.py                 # Django Forms (Loan Applications, Chat, etc.)
│   ├── models.py                # Database models (Users, Loans, Messages, News)
│   ├── signals.py               # Model signals
│   ├── templates/               # HTML Templates
│   │   └── sbapp/               # App-specific templates
│   ├── static/                  # Static assets (CSS, JS, Images)
│   └── views.py                 # Business logic
├── staticfiles/                 # Collected static files
├── theme/                       # UI Theme files (Tailwind, etc.)
├── requirements.txt             # Python dependencies
├── db.sqlite3                   # SQLite database (if used)
├── manage.py                    # Django CLI Management
└── terraform/                   # Terraform configuration for infrastructure
    ├── main.tf
    ├── provider.tf
    ├── outputs.tf
    └──  variables.tf
```

## Getting Started

### Prerequisites

- Python 3.12+
- pip & Virtualenv
- Docker (optional, for containerization)
- Azure CLI (for deploying to Azure)
- Terraform (for infrastructure management)

### Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your_username/fastapi_django.git
   cd fastapi_django/MySbaApp
   ```

2. **Create and Activate a Virtual Environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Database Migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Collect Static Files:**
   ```bash
   python manage.py collectstatic --noinput
   ```

6. **Run the Development Server:**
   ```bash
   python manage.py runserver
   ```

### Deployment

- **Docker:**  
  Build and run your container with the provided Dockerfile.

- **Azure Container Instances:**  
  Use the included `deploy.sh` script. Ensure proper configuration of environment variables (e.g., `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, etc.).  
  _Example Commands for Debugging:_
  ```bash
  az container logs --name "$CONTAINER_NAME" --resource-group "$RESOURCE_GROUP" --api-version "2024-11-01"
  az container attach --name "$CONTAINER_NAME" --resource-group "$RESOURCE_GROUP"
  ```

- **Terraform:**  
  Use Terraform scripts in the `terraform/` directory to provision infrastructure.Also, you need to create a terraform.tfvars file which will contain your ACI group, ACI registry, ACI container name, and ACI image name. It is not provided here because it contained private information.

### Environment Variables

Configure the following variables either directly in your environment or in a `.env` file:
- `SECRET_KEY`
- `DEBUG`
- `ALLOWED_HOSTS`
- `DATABASE_NAME`
- `MSSQL_ENGINE`
- `MSSQL_NAME`
- `MSSQL_USER`
- `MSSQL_PASSWORD`
- `MSSQL_HOST`
- `MSSQL_PORT`

## Debugging & Logging

- **Local:**  
  Django logs detailed error messages to the console.

- **Azure:**  
  Retrieve container logs or attach to your container for real-time debugging:
  ```bash
  az container logs --name "$CONTAINER_NAME" --resource-group "$RESOURCE_GROUP" --api-version "2024-11-01"
  az container attach --name "$CONTAINER_NAME" --resource-group "$RESOURCE_GROUP"
  ```

## Contributing

Contributions are welcome!  
1. **Fork the Project**  
2. **Create a Feature Branch**: `git checkout -b feature/new-feature`  
3. **Commit Your Changes**  
4. **Push to Your Branch**: `git push origin feature/new-feature`  
5. **Open a Pull Request**

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Author

This project was completed by [Michael Adebayo](https://github.com/MichAdebayo) 💻🚀