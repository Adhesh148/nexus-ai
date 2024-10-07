## NexusAI - AI-Powered Centralized Project Management Hub

NexusAI is a centralized project management platform that enhances team collaboration, automates repetitive tasks, and delivers persona-specific insights using AI. The platform integrates with Confluence, Jira, and other key tools to streamline software development life cycles, offering a cost-effective alternative to existing tools.

### Key Features

* Enhanced Knowledge Base Management
    - **Ingestion and Organization:** Automatically ingests and organizes documents from Confluence.
    - **Custom Uploads:** Users can upload documents, audios, and images to the project's knowledge base.

* AI-Powered Persona-Specific Chat Interface
    - **Role-Specific Insights:** Users can query the knowledge base, receiving responses tailored to their roles (e.g., developers, managers, QA).
* Intelligent Jira Ticket Creation
    - **Automated Ticket Creation:** Automatically creates Jira tickets from requirement documents and meeting notes uploaded to the knowledge base.
* Automated Release Notes Generation
    - **Template-Based Creation:** Allows users to store and reuse release note templates for consistent and professional documentation.

## Screenshots & Demo


Demo Link:
https://youtu.be/S1Il1N139XE

## Local Setup

### Prerequisites
* Python 3.x
* Docker
* Docker Compose
* Node.js & npm (for frontend)

### Folder Structure
```
nexus-backend/
│   ├── nexus-service/        # Core services containing APIs, core logic
│   ├── onboarding/           # Contains lambda code for user onboarding and Confluence ingestion
nexus-frontend/               # React-based frontend application
sandbox-tools/                
│   ├── .localstack/          # Scripts and configuration for setting up LocalStack
docker-compose.yml            # All necessary dependencies (e.g., localstack, opensearch)
```
### Setup local dependencies using Docker
This project leverages LocalStack for DynamoDB emulation and OpenSearch for search capabilities. These dependencies can be set up locally using Docker Compose, ensuring a smooth development environment that mirrors production.

To set up these dependencies, use the following command:

```sh
docker-compose up --build -d
```

### Running Frontend Locally

1. Install frontend dependencies and run application

```sh
cd nexus-frontend
npm install
npm start
```

### Running Backend Locally

```sh
# Create a Python virtual environment
python -m venv venv
source venv/bin/activate  # For Windows use: venv\Scripts\activate

cd nexuse-backend/nexus-service/

# Install required dependencies
pip install -r requirements.txt

# Run the application
cd src/
python server.py
```

### VSCode Setup

Add the following configurations in vscode:

1. launch.json

```json
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python Debugger: Current File",
            "type": "debugpy",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "env": {"PYTHONPATH": "{PATH_TO_PROJECT}/nexus/nexus-backend/nexus-service/src/"}
        }
    ]
}
```

2. settings.json

```json
{
    "python.analysis.extraPaths": [
        "{PATH_TO_PROJECT}/nexus/nexus-backend/nexus-service/src/"
    ]
}
```
