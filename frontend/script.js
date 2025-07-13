// Global variables
let currentEditingTaskId = null;
let refreshInterval = null;
let apiBaseUrl = window.API_CONFIG?.BASE_URL || 'http://localhost:8000';

// Test backend connectivity
async function testBackendConnection() {
    try {
        console.log('Testing backend connection...');
        const response = await fetch(`${apiBaseUrl}/`);
        if (response.ok) {
            const data = await response.json();
            console.log('✅ Backend is reachable:', data);
            showNotification('Backend connection successful!', 'success');
            return true;
        } else {
            console.log('❌ Backend responded with error:', response.status);
            showNotification(`Backend error: ${response.status}`, 'error');
            return false;
        }
    } catch (error) {
        console.log('❌ Cannot reach backend:', error);
        showNotification('Cannot reach backend server. Please start the backend first.', 'error');
        return false;
    }
}

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    loadSettings();
    
    // Test backend connection before loading dashboard
    testBackendConnection().then(isConnected => {
        if (isConnected) {
            loadDashboard();
            setupAutoRefresh();
        } else {
            // Show connection instructions
            showNotification('Backend not running. Please start the backend server first.', 'error');
        }
    });
    
    // Close modals when clicking outside
    window.onclick = function(event) {
        const createModal = document.getElementById('createTaskModal');
        const editModal = document.getElementById('editTaskModal');
        if (event.target === createModal) {
            closeCreateTaskModal();
        }
        if (event.target === editModal) {
            closeEditTaskModal();
        }
    };
});

// Navigation
function showSection(sectionId) {
    // Hide all sections
    const sections = document.querySelectorAll('.section');
    sections.forEach(section => section.classList.remove('active'));
    
    // Show selected section
    document.getElementById(sectionId).classList.add('active');
    
    // Update navigation
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => item.classList.remove('active'));
    event.target.closest('.nav-item').classList.add('active');
    
    // Load section-specific data
    switch(sectionId) {
        case 'dashboard':
            loadDashboard();
            break;
        case 'tasks':
            loadTasks();
            break;
        case 'metrics':
            loadMetrics();
            break;
    }
}

// API calls
async function apiCall(endpoint, options = {}) {
    try {
        showLoading();
        const url = `${apiBaseUrl}${endpoint}`;
        const requestOptions = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        };
        
        console.log('Making API call to:', url);
        console.log('Request options:', requestOptions);
        
        const response = await fetch(url, requestOptions);
        
        console.log('Response status:', response.status);
        console.log('Response headers:', response.headers);
        
        if (!response.ok) {
            const errorText = await response.text();
            console.error('Response error:', errorText);
            throw new Error(`HTTP error! status: ${response.status} - ${errorText}`);
        }
        
        const data = await response.json();
        console.log('Response data:', data);
        return data;
    } catch (error) {
        console.error('API Error:', error);
        
        // More detailed error message
        let errorMessage = 'API Error: ';
        if (error.message.includes('Failed to fetch')) {
            errorMessage += 'Cannot connect to backend server. Please check if the backend is running on ' + apiBaseUrl;
        } else {
            errorMessage += error.message;
        }
        
        showNotification(errorMessage, 'error');
        throw error;
    } finally {
        hideLoading();
    }
}

// Load dashboard data
async function loadDashboard() {
    try {
        const [stats, tasks] = await Promise.all([
            apiCall('/stats'),
            apiCall('/tasks')
        ]);
        
        updateStats(stats);
        updateRecentTasks(tasks.slice(0, 5)); // Show only 5 recent tasks
    } catch (error) {
        console.error('Failed to load dashboard:', error);
    }
}

// Update statistics
function updateStats(stats) {
    document.getElementById('total-tasks').textContent = stats.total_tasks;
    document.getElementById('pending-tasks').textContent = stats.pending_tasks;
    document.getElementById('completed-tasks').textContent = stats.completed_tasks;
    document.getElementById('completion-rate').textContent = 
        stats.completion_rate.toFixed(1) + '%';
}

// Update recent tasks
function updateRecentTasks(tasks) {
    const container = document.getElementById('recent-tasks-list');
    
    if (tasks.length === 0) {
        container.innerHTML = '<p style="color: #666; text-align: center; padding: 2rem;">No tasks found</p>';
        return;
    }
    
    container.innerHTML = tasks.map(task => `
        <div class="task-item">
            <div class="task-info">
                <div class="task-title">${escapeHtml(task.title)}</div>
                <div class="task-description">${escapeHtml(task.description || 'No description')}</div>
                <div class="task-meta">
                    <span class="task-status ${task.status}">${task.status}</span>
                    <span>Created: ${formatDate(task.created_at)}</span>
                    ${task.updated_at ? `<span>Updated: ${formatDate(task.updated_at)}</span>` : ''}
                </div>
            </div>
            <div class="task-actions">
                <button class="btn btn-secondary" onclick="editTask(${task.id})">
                    <i class="fas fa-edit"></i>
                </button>
                <button class="btn btn-danger" onclick="deleteTask(${task.id})">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        </div>
    `).join('');
}

// Load all tasks
async function loadTasks() {
    try {
        const filter = document.getElementById('status-filter').value;
        const endpoint = filter ? `/tasks?status=${filter}` : '/tasks';
        const tasks = await apiCall(endpoint);
        
        updateTasksGrid(tasks);
    } catch (error) {
        console.error('Failed to load tasks:', error);
    }
}

// Update tasks grid
function updateTasksGrid(tasks) {
    const container = document.getElementById('tasks-grid');
    
    if (tasks.length === 0) {
        container.innerHTML = '<p style="color: #666; text-align: center; padding: 2rem; grid-column: 1/-1;">No tasks found</p>';
        return;
    }
    
    container.innerHTML = tasks.map(task => `
        <div class="task-card">
            <div class="task-info">
                <div class="task-title">${escapeHtml(task.title)}</div>
                <div class="task-description">${escapeHtml(task.description || 'No description')}</div>
                <div class="task-meta">
                    <span class="task-status ${task.status}">${task.status}</span>
                    <span>Created: ${formatDate(task.created_at)}</span>
                    ${task.updated_at ? `<span>Updated: ${formatDate(task.updated_at)}</span>` : ''}
                </div>
            </div>
            <div class="task-actions">
                <button class="btn btn-secondary" onclick="editTask(${task.id})">
                    <i class="fas fa-edit"></i>
                    Edit
                </button>
                <button class="btn btn-danger" onclick="deleteTask(${task.id})">
                    <i class="fas fa-trash"></i>
                    Delete
                </button>
            </div>
        </div>
    `).join('');
}

// Filter tasks
function filterTasks() {
    loadTasks();
}

// Create task modal
function showCreateTaskModal() {
    document.getElementById('createTaskModal').style.display = 'block';
    document.getElementById('taskTitle').focus();
}

function closeCreateTaskModal() {
    document.getElementById('createTaskModal').style.display = 'none';
    document.getElementById('createTaskForm').reset();
}

// Create task
async function createTask() {
    const title = document.getElementById('taskTitle').value.trim();
    const description = document.getElementById('taskDescription').value.trim();
    const status = document.getElementById('taskStatus').value;
    
    if (!title) {
        showNotification('Please enter a task title', 'error');
        return;
    }
    
    try {
        const taskData = {
            title,
            description: description || null,
            status
        };
        
        await apiCall('/tasks', {
            method: 'POST',
            body: JSON.stringify(taskData)
        });
        
        closeCreateTaskModal();
        showNotification('Task created successfully!', 'success');
        refreshData();
    } catch (error) {
        console.error('Failed to create task:', error);
    }
}

// Edit task modal
async function editTask(taskId) {
    try {
        const task = await apiCall(`/tasks/${taskId}`);
        
        currentEditingTaskId = taskId;
        document.getElementById('editTaskTitle').value = task.title;
        document.getElementById('editTaskDescription').value = task.description || '';
        document.getElementById('editTaskStatus').value = task.status;
        
        document.getElementById('editTaskModal').style.display = 'block';
        document.getElementById('editTaskTitle').focus();
    } catch (error) {
        console.error('Failed to load task:', error);
    }
}

function closeEditTaskModal() {
    document.getElementById('editTaskModal').style.display = 'none';
    document.getElementById('editTaskForm').reset();
    currentEditingTaskId = null;
}

// Update task
async function updateTask() {
    if (!currentEditingTaskId) return;
    
    const title = document.getElementById('editTaskTitle').value.trim();
    const description = document.getElementById('editTaskDescription').value.trim();
    const status = document.getElementById('editTaskStatus').value;
    
    if (!title) {
        showNotification('Please enter a task title', 'error');
        return;
    }
    
    try {
        const taskData = {
            title,
            description: description || null,
            status
        };
        
        await apiCall(`/tasks/${currentEditingTaskId}`, {
            method: 'PUT',
            body: JSON.stringify(taskData)
        });
        
        closeEditTaskModal();
        showNotification('Task updated successfully!', 'success');
        refreshData();
    } catch (error) {
        console.error('Failed to update task:', error);
    }
}

// Delete task
async function deleteTask(taskId) {
    if (!confirm('Are you sure you want to delete this task?')) return;
    
    try {
        await apiCall(`/tasks/${taskId}`, {
            method: 'DELETE'
        });
        
        showNotification('Task deleted successfully!', 'success');
        refreshData();
    } catch (error) {
        console.error('Failed to delete task:', error);
    }
}

// Load metrics
async function loadMetrics() {
    try {
        const metrics = await fetch(`${apiBaseUrl}/metrics`);
        const metricsText = await metrics.text();
        
        // For now, just show that metrics are available
        showNotification('Metrics loaded successfully!', 'info');
        console.log('Metrics:', metricsText);
    } catch (error) {
        console.error('Failed to load metrics:', error);
        showNotification('Failed to load metrics', 'error');
    }
}

// Refresh all data
async function refreshData() {
    const activeSection = document.querySelector('.section.active');
    const sectionId = activeSection.id;
    
    switch(sectionId) {
        case 'dashboard':
            await loadDashboard();
            break;
        case 'tasks':
            await loadTasks();
            break;
        case 'metrics':
            await loadMetrics();
            break;
    }
    
    showNotification('Data refreshed!', 'info');
}

// Auto refresh
function setupAutoRefresh() {
    const intervalSeconds = parseInt(document.getElementById('refresh-interval').value) || 30;
    
    if (refreshInterval) {
        clearInterval(refreshInterval);
    }
    
    refreshInterval = setInterval(() => {
        refreshData();
    }, intervalSeconds * 1000);
}

// Settings
function loadSettings() {
    const savedApiUrl = localStorage.getItem('apiBaseUrl');
    const savedInterval = localStorage.getItem('refreshInterval');
    
    if (savedApiUrl) {
        apiBaseUrl = savedApiUrl;
        document.getElementById('api-url').value = savedApiUrl;
    }
    
    if (savedInterval) {
        document.getElementById('refresh-interval').value = savedInterval;
    }
}

function saveSettings() {
    const apiUrl = document.getElementById('api-url').value.trim();
    const interval = document.getElementById('refresh-interval').value;
    
    if (!apiUrl) {
        showNotification('Please enter API URL', 'error');
        return;
    }
    
    apiBaseUrl = apiUrl;
    localStorage.setItem('apiBaseUrl', apiUrl);
    localStorage.setItem('refreshInterval', interval);
    
    setupAutoRefresh();
    showNotification('Settings saved!', 'success');
}

// Utility functions
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
}

function showLoading() {
    document.getElementById('loading').style.display = 'flex';
}

function hideLoading() {
    document.getElementById('loading').style.display = 'none';
}

function showNotification(message, type = 'info') {
    const notification = document.getElementById('notification');
    notification.textContent = message;
    notification.className = `notification ${type} show`;
    
    setTimeout(() => {
        notification.classList.remove('show');
    }, 3000);
}

// Keyboard shortcuts
document.addEventListener('keydown', function(event) {
    // Ctrl/Cmd + N to create new task
    if ((event.ctrlKey || event.metaKey) && event.key === 'n') {
        event.preventDefault();
        showCreateTaskModal();
    }
    
    // Escape to close modals
    if (event.key === 'Escape') {
        closeCreateTaskModal();
        closeEditTaskModal();
    }
    
    // Ctrl/Cmd + R to refresh
    if ((event.ctrlKey || event.metaKey) && event.key === 'r') {
        event.preventDefault();
        refreshData();
    }
});

// Handle form submissions
document.getElementById('createTaskForm').addEventListener('submit', function(event) {
    event.preventDefault();
    createTask();
});

document.getElementById('editTaskForm').addEventListener('submit', function(event) {
    event.preventDefault();
    updateTask();
});

// Mobile menu toggle (for responsive design)
function toggleMobileMenu() {
    const sidebar = document.querySelector('.sidebar');
    sidebar.classList.toggle('open');
}

// Add mobile menu button if needed
if (window.innerWidth <= 768) {
    const header = document.querySelector('.header');
    const menuButton = document.createElement('button');
    menuButton.className = 'btn btn-secondary mobile-menu-btn';
    menuButton.innerHTML = '<i class="fas fa-bars"></i>';
    menuButton.onclick = toggleMobileMenu;
    header.querySelector('.header-actions').prepend(menuButton);
}

// Handle window resize
window.addEventListener('resize', function() {
    if (window.innerWidth > 768) {
        document.querySelector('.sidebar').classList.remove('open');
    }
});

// Service worker for offline support (optional)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        navigator.serviceWorker.register('/sw.js').then(function(registration) {
            console.log('ServiceWorker registration successful');
        }).catch(function(error) {
            console.log('ServiceWorker registration failed');
        });
    });
} 