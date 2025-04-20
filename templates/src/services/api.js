const API_BASE_URL = '/api';

export const taskService = {
    // Create a new task
    createTask: async (taskData) => {
        try {
            const response = await fetch(`${API_BASE_URL}/task`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(taskData),
                credentials: 'include' // This is important for handling sessions
            });

            if (!response.ok) {
                throw new Error('Failed to create task');
            }

            return await response.json();
        } catch (error) {
            console.error('Error creating task:', error);
            throw error;
        }
    },

    // Get all tasks for the current user
    getTasks: async () => {
        try {
            console.log("Fetching tasks...");
            const response = await fetch(`${API_BASE_URL}/tasks`, {
                credentials: 'include'
            });

            if (!response.ok) {
                throw new Error('Failed to fetch tasks');
            }

            const data = await response.json();
            console.log("Fetched tasks:", data);
            return data;
        } catch (error) {
            console.error('Error fetching tasks:', error);
            throw error;
        }
    },

    // Get AI suggestions for task
    getAISuggestions: async (userInput) => {
        try {
            const response = await fetch(`${API_BASE_URL}/prompt/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: userInput }),
                credentials: 'include'
            });

            if (!response.ok) {
                throw new Error('Failed to get AI suggestions');
            }

            return await response.json();
        } catch (error) {
            console.error('Error getting AI suggestions:', error);
            throw error;
        }
    },

    // Send raw user input to backend
    sendTaskRequest: async (userInput) => {
        try {
            const response = await fetch(`${API_BASE_URL}/prompt/command`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ input: userInput }),
                credentials: 'include'
            });

            if (!response.ok) {
                throw new Error('Request failed');
            }

            return await response.json();
        } catch (error) {
            console.error('Error processing request:', error);
            throw error;
        }
    }
};

export const authService = {
    // Check login status
    checkAuth: async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/auth/status`, {
                credentials: 'include'
            });
            return await response.json();
        } catch (error) {
            console.error('Error checking auth status:', error);
            throw error;
        }
    },

    // Handle logout
    logout: async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/auth/logout`, {
                method: 'POST',
                credentials: 'include'
            });
            return await response.json();
        } catch (error) {
            console.error('Error during logout:', error);
            throw error;
        }
    }
};
