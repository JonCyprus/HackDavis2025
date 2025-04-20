import { useState, useEffect } from "react";
import { taskService, authService } from './services/api';
import './App.css';

function App() {
  const [state, setState] = useState('notLoggedInHome');
  const [tasks, setTasks] = useState([]);
  const [userInput, setUserInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  // Check auth status on mount
  useEffect(() => {
    const checkAuthStatus = async () => {
      try {
        const status = await authService.checkAuth();
        if (status.authenticated) {
          setState('home');
          loadTasks();
        }
      } catch (error) {
        console.error('Auth check failed:', error);
      }
    };
    
    checkAuthStatus();
  }, []);

  // Load tasks
  const loadTasks = async () => {
    try {
      const userTasks = await taskService.getTasks();
      setTasks(userTasks);
    } catch (error) {
      setError('Failed to load tasks');
    }
  };

  // Handle task input
  const handleTaskInput = async (e) => {
    if (e.key === 'Enter' && userInput.trim()) {
      setIsLoading(true);
      try {
        // Send raw input to backend
        const response = await taskService.sendTaskRequest(userInput);
        console.log('Server response:', response);
        
        // Handle response as needed
        if (response.success) {
          setState('task');
        }
        
        setUserInput('');
      } catch (error) {
        setError('Failed to process request');
      } finally {
        setIsLoading(false);
      }
    }
  };

  function Tasky(){
    return <img src="images/tasky-01.svg" className="tasky" alt="tasky, a fluffy yellow blob with big eyes" />;
  }

  const CloudBtn = (props) => {
    return <button className="cloudBtn" onClick={props.goToNewTask}>New Task</button>
  }

  const notLoggedInHomePg = (<div className="App">
    <header className="App-header">
      <h1>
        Welcome to Taskland!
      </h1>
    </header>
    <main className="notLoggedInHome">
      <h3>Make an account!</h3>
      <a href="/api/auth/login" className="login-btn">Log in</a>

      <div className="bg">
          <div className="hill1"></div>
          <div className="hill2"></div>
          <div className="hill3"></div>
      </div>
    </main>
  </div>);
  
  const logInPg = (<div className="App">
    <header className="App-header">
      <h1>
        Log in to Taskland
      </h1>
    </header>
    <main className="home">
      <p>insert login stuff here</p>
    </main>
  </div>);

  const homePg = (<div className="App">
    <header className="App-header">
      <h1>
        Taskland
      </h1>
    </header>
    <main className="home">
      <CloudBtn goToNewTask={() => setState('newTask')}/>
      
      <div className="bg">
          <div className="hill1"></div>
          <div className="hill2"></div>
          <div className="hill3"></div>
      </div>
    </main>
  </div>);

  const newTaskPg = (<div className="App">
      <main className="newTask">
        <div className="taskyZone">
          <div className="dialog">
            {error && <p className="error">{error}</p>}
            {isLoading && <p>Thinking...</p>}
          </div>
          <Tasky />
        </div>
        <input
          name="talkToTasky"
          type="text"
          value={userInput}
          onChange={(e) => setUserInput(e.target.value)}
          onKeyPress={handleTaskInput}
          placeholder="Tell me about your task..."
        />
      </main>
  </div>);

// note: below page is static text, will be replaced with user inputs
  const taskPg = (<div className="App">
    <main className="task">
      {tasks.map(task => (
        <div key={task.id} className="task-item">
          <h1>{task.title}</h1>
          <span className="day">{task.date}</span> <span className="time">{task.time}</span>

          <h3>Desctiption:</h3>
          <p>{task.description}</p>

          <h2>Steps:</h2>
            <div className="subtask">{task.steps?.map((step, index) => (
              <div key={index} className="subtask">{step}</div>
            ))}</div>
        </div>
      ))}
    </main>
    <div className="taskyCircle">
        <Tasky />
    </div>
  </div>);

switch(state){
  case "notLoggedInHome":
    return notLoggedInHomePg;
  case "login":
    return logInPg;
  case "home":
    return homePg;
  case "newTask":
    return newTaskPg;
  case "task":
    return taskPg;
  default:
    return notLoggedInHomePg;
}

}

export default App;
