# Developer Notifier

The main purpose of this project is to fetch and display:

1. GitHub pull requests assigned to the user
2. GitHub pull requests where the user is requested for review
3. Jira issues assigned to the user

This application serves as a centralized dashboard for developers to keep track of their tasks and review requests across different platforms, enhancing productivity and workflow management.

## Prerequisites

- Python 3.12+
- Node.js 20+
- Docker (optional)

## Getting Started

### Docker Setup

To run the entire application using Docker:

1. Ensure Docker and Docker Compose are installed on your system.

2. Build and start the containers:

   ```
   docker-compose up -d --build
   ```

3. Access the application at `http://localhost:8080`

### Backend Setup

1. Navigate to the `backend` directory:

   ```
   cd backend
   ```

2. Create a virtual environment and activate it:

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

4. Set up your environment variables by copying `.env.example` to `.env` and modifying as needed:

   ```
   cp .env.example .env
   ```

5. Run database migrations:

   ```
   alembic upgrade head
   ```

6. Start the FastAPI server:
   ```
   fastapi dev app/main.py
   ```

### Frontend Setup

1. Navigate to the `frontend` directory:

   ```
   cd frontend
   ```

2. Install dependencies:

   ```
   npm install
   ```

3. Start the Nuxt.js development server:
   ```
   npm run dev
   ```

## Project Structure

- `backend/`: FastAPI application
  - `app/`: Main application code
  - `alembic/`: Database migration scripts
- `frontend/`: Nuxt.js application
- `docker-compose.yml`: Docker composition file

## Application Setup

1. Ensure both the backend and frontend servers are running as described in the setup sections above.

2. Open your web browser and navigate to:

   ```
   http://localhost:3000 or http://localhost:8080 (if you are using Docker)
   ```

   This will open the frontend application, which communicates with the backend API.

3. You will see the main page with the message: Settings not found. Please configure your settings.

4. Click on the "Open Settings" button in the top menu.

5. Enter your GitHub and Jira credentials:

   - Jira API Email:
   - Jira API Key:
   - Jira API URL:
   - GitHub Access Token:
   - GitHub Organization:
   - GitHub API URL:
   - GitHub User:
   - User Name:

Note:

- You can get the GitHub Access Token from [here](https://github.com/settings/tokens).
- You can get the Jira API Key from [here](https://id.atlassian.com/manage-profile/security/api-tokens).

## License

This project is licensed under the WTFPL License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
