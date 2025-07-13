# Tasky Frontend Dashboard

A modern, responsive web dashboard for the Tasky task management API.

## Features

- 📊 **Dashboard Overview**: Real-time statistics and recent tasks
- ✅ **Task Management**: Create, read, update, and delete tasks
- 📈 **Metrics Integration**: View system metrics and Grafana dashboards
- 🎨 **Modern UI**: Dark theme with smooth animations
- 📱 **Responsive Design**: Works on desktop, tablet, and mobile
- ⚡ **Real-time Updates**: Auto-refresh functionality
- ⌨️ **Keyboard Shortcuts**: Quick actions with keyboard shortcuts

## Quick Start

### 🐳 Docker (Recommended)

1. **Start the Backend API** (from the project root):
   ```bash
   cd ..
   python -m uvicorn app.main:app --reload
   ```

2. **Run Frontend with Docker**:
   ```bash
   # Linux/Mac
   ./run-docker.sh
   
   # Windows
   run-docker.bat
   
   # Or manually
   docker build -t tasky-frontend .
   docker run -d --name tasky-frontend --rm -p 3001:3001 tasky-frontend
   ```

3. **Open in Browser**:
   Navigate to `http://localhost:3001`

### 🐍 Python (Alternative)

1. **Start the Backend API** (from the project root):
   ```bash
   cd ..
   python -m uvicorn app.main:app --reload
   ```

2. **Start the Frontend Server**:
   ```bash
   python server.py
   ```

3. **Open in Browser**:
   Navigate to `http://localhost:3001`

### 🐳 Complete Stack with Docker Compose

Run the entire application stack (backend, frontend, monitoring) with Docker Compose:

```bash
# From the project root
docker-compose up -d

# Or build and run
docker-compose up --build -d
```

**Access URLs:**
- Frontend: http://localhost:3001
- Backend: http://localhost:8000
- Grafana: http://localhost:3000
- Prometheus: http://localhost:9090
- APISIX Gateway: http://localhost:9080

## Dashboard Sections

### 🏠 Dashboard
- Overview statistics (total, pending, completed tasks, completion rate)
- Recent tasks with quick actions
- Visual cards with color-coded metrics

### 📋 Tasks
- Complete task list with filtering options
- Create new tasks with the "New Task" button
- Edit and delete tasks inline
- Filter by status (All, Pending, Done)

### 📊 Metrics
- System performance metrics
- Links to Grafana dashboards
- Raw Prometheus metrics access

### ⚙️ Settings
- Configure API base URL
- Set auto-refresh interval
- Persistent settings storage

## Keyboard Shortcuts

- `Ctrl/Cmd + N`: Create new task
- `Ctrl/Cmd + R`: Refresh data
- `Escape`: Close modals

## API Integration

The frontend integrates with all backend endpoints:

- `GET /tasks` - Fetch all tasks
- `POST /tasks` - Create new task
- `GET /tasks/{id}` - Get specific task
- `PUT /tasks/{id}` - Update task
- `DELETE /tasks/{id}` - Delete task
- `GET /stats` - Get statistics
- `GET /metrics` - Get Prometheus metrics

## Configuration

### API Base URL
Default: `http://localhost:8000`

You can change this in the Settings section or by modifying the `apiBaseUrl` variable in `script.js`.

### Auto-refresh
Default: 30 seconds

Configurable in the Settings section. Set to 0 to disable auto-refresh.

## Browser Support

- Chrome 70+
- Firefox 60+
- Safari 12+
- Edge 79+

## File Structure

```
frontend/
├── index.html          # Main HTML file
├── styles.css          # CSS styles
├── script.js           # JavaScript functionality
├── server.py           # Static file server
└── README.md           # This file
```

## Development

### Running with Custom Port

```bash
python server.py 8080
```

### CORS Configuration

The frontend server includes CORS headers to allow API calls to the backend. If you encounter CORS issues, ensure:

1. The backend API is running on `http://localhost:8000`
2. The frontend server is running on `http://localhost:3001`
3. Both servers are accessible from your browser

## Features in Detail

### Statistics Cards
- **Total Tasks**: Shows the complete number of tasks
- **Pending Tasks**: Tasks with "pending" status
- **Completed Tasks**: Tasks with "done" status  
- **Completion Rate**: Percentage of completed tasks

### Task Management
- **Create Task**: Modal with title, description, and status
- **Edit Task**: Update existing tasks
- **Delete Task**: Remove tasks with confirmation
- **Status Toggle**: Quick status changes
- **Filtering**: Filter tasks by status

### Responsive Design
- Mobile-friendly interface
- Collapsible sidebar on mobile
- Touch-friendly buttons and controls
- Adaptive grid layouts

### Real-time Updates
- Auto-refresh every 30 seconds (configurable)
- Manual refresh button
- Live statistics updates
- Instant UI feedback

## Troubleshooting

### Common Issues

1. **API Connection Failed**
   - Ensure backend is running on `http://localhost:8000`
   - Check CORS configuration
   - Verify network connectivity

2. **Frontend Not Loading**
   - Ensure frontend server is running
   - Check browser console for errors
   - Try clearing browser cache

3. **Tasks Not Updating**
   - Check auto-refresh settings
   - Manually refresh the page
   - Verify API endpoints are responding

### Debug Mode

Open browser developer tools (F12) to see:
- Console logs for API calls
- Network requests and responses
- JavaScript errors

### Docker Troubleshooting

**Container won't start:**
```bash
# Check logs
docker logs tasky-frontend

# Check if port is in use
netstat -tlnp | grep 3001

# Remove existing container
docker rm -f tasky-frontend
```

**API connection issues in Docker:**
```bash
# Check if backend is reachable from container
docker exec tasky-frontend curl -f http://localhost:8000/

# Check network connectivity
docker network ls
docker network inspect tasky-network
```

**Rebuild after changes:**
```bash
# Stop and remove container
docker stop tasky-frontend
docker rmi tasky-frontend

# Rebuild and run
docker build -t tasky-frontend .
docker run -d --name tasky-frontend --rm -p 3001:3001 tasky-frontend
```

## Contributing

Feel free to enhance the dashboard with:
- Additional visualizations
- More keyboard shortcuts
- Enhanced mobile experience
- Dark/light theme toggle
- Task categories or tags
- Export functionality 