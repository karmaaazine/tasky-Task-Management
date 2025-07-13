# Tasky - Task Management API

A comprehensive Task Management API built with FastAPI, featuring monitoring, testing, and API gateway capabilities.

## 🚀 Features

- **CRUD Operations**: Create, read, update, and delete tasks
- **Task Filtering**: Filter tasks by status (pending, done)
- **Metrics & Monitoring**: Prometheus metrics and Grafana dashboards
- **API Gateway**: Apache APISIX for API management
- **Testing**: Comprehensive pytest test suite with coverage
- **CI/CD**: GitHub Actions workflow for automated testing and deployment

## 🛠️ Tech Stack

- **Backend**: FastAPI
- **Testing**: Pytest + Coverage
- **Monitoring**: Prometheus + Grafana
- **API Gateway**: Apache APISIX
- **Containerization**: Docker + Docker Compose
- **CI/CD**: GitHub Actions

## 📦 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome message |
| GET | `/tasks` | Get all tasks (with optional status filter) |
| POST | `/tasks` | Create a new task |
| GET | `/tasks/{id}` | Get a specific task |
| PUT | `/tasks/{id}` | Update a task |
| DELETE | `/tasks/{id}` | Delete a task |
| GET | `/metrics` | Prometheus metrics |
| GET | `/stats` | Task statistics |

## 🏃‍♂️ Quick Start

### Prerequisites
- Docker and Docker Compose
- Python 3.11+ (for local development)

### Running with Docker Compose

1. Clone the repository:
```bash
git clone <repository-url>
cd tasky
```

2. Start all services:
```bash
docker-compose up -d
```

3. Access the services:
- **API**: http://localhost:8000
- **API Gateway (APISIX)**: http://localhost:9080
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (admin/admin)

### Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
uvicorn app.main:app --reload
```

3. Run tests:
```bash
pytest tests/ -v
```

4. Run tests with coverage:
```bash
pytest tests/ --cov=app --cov-report=term-missing
```

## 📊 Monitoring

### Prometheus Metrics
- HTTP request counts and duration
- Task statistics (total, completed, pending)
- Application information

### Grafana Dashboards
- API performance metrics
- Task management statistics
- System health monitoring

## 🧪 Testing

The project includes comprehensive test coverage:

- API endpoint testing
- Input validation testing
- Error handling testing
- Metrics endpoint testing

Run tests with:
```bash
pytest tests/ -v --cov=app
```

## 🔧 Configuration

### Environment Variables
- `PYTHONPATH`: Set to include the app directory

### Configuration Files
- `prometheus.yml`: Prometheus configuration
- `apisix.yml`: Apache APISIX configuration
- `docker-compose.yml`: Multi-service orchestration

## 📈 Usage Examples

### Create a Task
```bash
curl -X POST "http://localhost:8000/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete project documentation",
    "description": "Write comprehensive README and API docs",
    "status": "pending"
  }'
```

### Get All Tasks
```bash
curl "http://localhost:8000/tasks"
```

### Filter Tasks by Status
```bash
curl "http://localhost:8000/tasks?status=pending"
```

### Update a Task
```bash
curl -X PUT "http://localhost:8000/tasks/1" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "done"
  }'
```

### Get Task Statistics
```bash
curl "http://localhost:8000/stats"
```

## 🔒 Security

- Input validation using Pydantic models
- Vulnerability scanning with Trivy in CI/CD
- Health checks for all services

## 🚀 Deployment

The application is designed for containerized deployment:

1. **Development**: Use `docker-compose up` for local development
2. **Production**: Deploy containers to your preferred orchestration platform
3. **CI/CD**: GitHub Actions workflow handles testing and building

## 📝 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## 📞 Support

For issues and questions, please create an issue in the GitHub repository. 