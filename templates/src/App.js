import { useState, useEffect } from "react";
import { taskService, authService } from './services/api';
import './App.css';

function App() {
  const [state, setState] = useState('notLoggedInHome');
  const [tasks, setTasks] = useState([]);
  const [userInput, setUserInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const[resp, setResp] = useState("Heya, I'm Tasky, and I'm here to help you complete your tasks!")

  // Manual task creation
  const [title, setTitle] = useState("")
  const [description, setDescription] = useState("")
  const [date, setDate] = useState("")
  const [time, setTime] = useState("")

  const NavBar = () => (
  <div className="navBar">
    <select
      value={state}
      onChange={(e) => setState(e.target.value)}
    >
      <option value="home">🏠 Home</option>
      <option value="taskyCommand">➕ New Task (AI)</option>
      <option value="manualTask">✍️ Manual Task</option>
      <option value="task">📋 Task List</option>
      <option value="taskyTalk">💬 Talk to Tasky</option>
    </select>
  </div>
);

  // Functions
  // For the manual task creation
    const handleCreate = async () => {
  if (!title || !description || !date || !time) {
    setError("Please fill out all fields.");
    return;
  }

  const task = { title, description, date, time };

  try {
    const response = await taskService.createTask(task);
    if (response.success) {
      setState("task");
    } else {
      setError("Task creation failed.");
    }
  } catch (err) {
    setError("Server error.");
  }
};

  // Check auth status on mount
  useEffect(() => {
    const checkAuthStatus = async () => {
      try {
        const status = await authService.checkAuth();
        if (status.authenticated) {
          setState('home');
          await taskService.getTasks();
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

  useEffect(() => {
    const maybeLoadTasks = async () => {
      if (state === 'task') {
        const fetchedTasks = await taskService.getTasks();
        setTasks(fetchedTasks);
      }
    };
  
    maybeLoadTasks();
  }, [state]);

  // Handle task input
  const handleTaskyChat = async (e) => {
    if (e.key === 'Enter' && userInput.trim()) {
      setIsLoading(true);
      try {
        // Send raw input to backend
        console.log('User input is: ', userInput)
        const apiResp = await taskService.getAISuggestions(userInput);
        console.log('Server response:', apiResp);
        setResp(apiResp.response)
        console.log('resp extract: ', apiResp.response)
        
        // Handle response as needed
        if (apiResp.success) {
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

  const handleTaskyCommand = async (e) => {
    if (e.key === 'Enter' && userInput.trim()) {
      setIsLoading(true);
      try {
        // Send raw input to backend
        console.log('User input is: ', userInput)
        const apiResp = await taskService.sendTaskRequest(userInput);
        console.log('Server response:', apiResp);
        setResp(apiResp.response)
        console.log('resp extract: ', apiResp.response)
        
        // Handle response as needed
        if (apiResp.success) {
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
    const taskySprites = [(<img src="images/tasky-01.svg" className="tasky" alt="tasky, a fluffy yellow blob with big eyes" />), (<img src="images/tasky-02.svg" className="tasky" alt="tasky, a fluffy yellow blob, looks pensive" />), (<img src="images/tasky-03.svg" className="tasky" alt="tasky, a fluffy yellow blob, looks excited!" />)]
    return taskySprites[0];
  }

  const CloudBtn = (props) => {
    return <button className="cloudBtn" onClick={props.goToTaskyCommand}>New Task</button>
  }

  const ManualTaskBtn = (props) => {
    return <button className="manualTaskBtn" onClick={props.goToManualTask}>Enter task manually</button>
  }

  const notLoggedInHomePg = (<div className="App">
    <header className="App-header">
      <h1>
        Welcome to Taskland!
      </h1>
    </header>
    <main className="notLoggedInHome">
      <h3>Make an account:</h3>
      <a href="/api/auth/login" className="login-btn">Log in</a>
    </main>
    <div className="bg">
          <div className="hill1"></div>
          <div className="hill2"></div>
          <div className="hill3"></div>
    </div>
  </div>);

  const homePg = (<div className="App">
    <header className="App-header">
      <h1>
        Taskland
      </h1>
    </header>
    <main className="home">
      <CloudBtn goToTaskyCommand={() => setState('taskyCommand')}/>
    </main>

    <div className="bg">
          <div className="hill1"></div>
          <div className="hill2"></div>
          <div className="hill3"></div>
    </div>
  </div>);

const taskyCommand = (<div className="App">
  <main className="newTask">
      <div className="taskyZone">
        <div className="dialog">
          {error && <p className="error">{error}</p>}
          {isLoading && <p>Thonking...</p>}
          <p>{resp}</p>
        </div>
        <Tasky/>
      </div>
    <div className="taskForm">
      <input
          name="talkToTasky"
          type="text"
          value={userInput}
          onChange={(e) => setUserInput(e.target.value)}
          onKeyDown={handleTaskyCommand}
          placeholder="Tell me about your task ^-^"
      />
    </div>
    <p class="seperatorTxt">or...</p>
    <ManualTaskBtn goToManualTask={() => setState('manualTask')}/>
  </main>
  </div>);

const manualTaskPg = (
  <main className="manualTask">
    <div className="taskForm">
      <input
          type="text"
          placeholder="Title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
      />
      <input
          type="text"
          placeholder="Description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
      />
      <input
          type="text"
          placeholder="MM/DD/YYYY"
          value={date}
          onChange={(e) => setDate(e.target.value)}
      />
      <input
          type="text"
          placeholder="HH:MM (24hr)"
          value={time}
          onChange={(e) => setTime(e.target.value)}
      />
      <button onClick={handleCreate}>Create Task</button>
    </div>
  </main>
);

const taskyTalk = (<div className="App">
  <main className="newTask">
      <div className="taskyZone">
        <div className="dialog">
          {error && <p className="error">{error}</p>}
          {isLoading && <p>Thonking...</p>}
          <p>{resp}</p>
        </div>
        <Tasky/>
      </div>
    <div className="taskForm">
      <input
          name="talkToTasky"
          type="text"
          value={userInput}
          onChange={(e) => setUserInput(e.target.value)}
          onKeyDown={handleTaskyChat}
          placeholder="What do you need to know?"
      />
    </div>
  </main>
</div>);

const taskPg = (
  <div className="App">
    <main className="task">
    {tasks.length === 0 && <p>No tasks yet.</p>}
 
 {tasks.map((task, index) => (
   <div key={task.TASKID || index} className="task-item">
     <h2>{task.TITLE}</h2>

     {task.DESC ? (
       <p><strong>Description:</strong> {task.DESC}</p>
     ) : null}

     {task.steps?.length > 0 && (
       <div className="subtasks">
         <p><strong>Subtasks:</strong></p>
         <ul>
           {task.steps.map((step, idx) => (
             <li key={idx}>{step}</li>
           ))}
         </ul>
       </div>
     )}
   </div>
 ))}
</main>
    <div className="taskyCircle">
      <Tasky />
    </div>
  </div>
);


return (
  <>
    <NavBar />
    {(() => {
      switch (state) {
        case "notLoggedInHome":
          return notLoggedInHomePg;
        case "home":
          return homePg;
        case "manualTask":
          return manualTaskPg;
        case "task":
          return taskPg;
        case "taskyTalk":
          return taskyTalk;
        case "taskyCommand":
          return taskyCommand;
        default:
          return notLoggedInHomePg;
      }
    })()}
  </>
);
}

export default App;