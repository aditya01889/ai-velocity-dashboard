# AI Velocity Dashboard

A comprehensive monitoring tool for GenAI development teams, tracking productivity, cost, and risk metrics across your AI development lifecycle.

## Features

- **Team Velocity**: Track PR cycle times, commit activity, and contributor engagement
- **Prompt/Test Coverage**: Monitor prompt-to-test mapping and test run results
- **Infrastructure Cost Drift**: Visualize and alert on cost anomalies
- **Security Posture**: Detect misconfigurations and security risks

## Tech Stack

- **Backend**: Python, FastAPI
- **Frontend**: Streamlit (MVP), React (future)
- **Database**: SQLite (development), TimescaleDB (production)
- **Infrastructure**: Docker, AWS

## Getting Started

### Prerequisites

- Python 3.10+
- Docker (for containerized deployment)
- GitHub Personal Access Token
- LangSmith API Key (optional)
- AWS Credentials (for cost/security modules)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-org/ai-velocity-dashboard.git
   cd ai-velocity-dashboard
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file:
   ```bash
   cp .env.example .env
   # Update the .env file with your credentials
   ```

### Running the Dashboard

```bash
# Start the Streamlit dashboard
streamlit run app/main.py

# Or run with Docker
# docker-compose up --build
```

## Project Structure

```
ai-velocity-dashboard/
├── app/
│   ├── api/           # API endpoints
│   ├── core/          # Core application logic
│   ├── models/        # Data models
│   ├── services/      # Business logic and external service integrations
│   └── utils/         # Helper functions
├── config/            # Configuration files
├── tests/             # Test suite
├── .env.example       # Example environment variables
├── requirements.txt   # Python dependencies
└── README.md          # This file
```

## Development

### Setting Up for Development

1. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

2. Run tests:
   ```bash
   pytest
   ```

3. Format code:
   ```bash
   black .
   isort .
   ```

### Contributing

1. Create a new branch for your feature
2. Make your changes
3. Add tests for your changes
4. Submit a pull request

## License

MIT License - see the [LICENSE](LICENSE) file for details
