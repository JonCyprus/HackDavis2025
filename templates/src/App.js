import { useState } from "react";
import './App.css';

function App() {
  const [state, setState] = useState('notLoggedInHome');

  // useEffect(() => {
  //   fetch("/me")
  //     .then(res => res.json())
  //     .then(data => {
  //       setUser(data.user);
  //     });
  // }, []);
  
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
      <h3><a href="/login">Log in/Make an account!</a></h3>
      <div className="bg">
          <div className="hill1"></div>
          <div className="hill2"></div>
          <div className="hill3"></div>
      </div>
    </main>
  </div>);
  
  // const logInPg = (<div className="App">
  //   <header className="App-header">
  //     <h1>
  //       Log in to Taskland
  //     </h1>
  //   </header>
  //   <main className="logIn">
  //         <h2>Welcome session.name!</h2>
  //         <p><a href="/logout">Logout</a></p>
  //         <h2>Welcome Guest</h2>
  //         <p><a href="/login">Login</a></p>
  //   </main>
  // </div>);

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
          <div className="dialog"></div>
          <Tasky />
        </div>
        <input name="talkToTasky" type="text" />
      </main>
  </div>);

// note: below page is src text, will be replaced with user inputs
  const taskPg = (<div className="App">
    <main className="task">
      <h1>Task Name</h1>
      <span className="day">Day</span> <span className="time">Time</span>

      <h3>Desctiption:</h3>
      <p>Description</p>

      <h2>Steps:</h2>
        <div className="subtask">Subtask</div>
        <div className="subtask">Another one</div>
        <div className="subtask">I'll make subtasks a react object</div>
    </main>
    <div className="taskyCircle">
        <Tasky />
    </div>
  </div>);

switch(state){
  case "notLoggedInHome":
    return notLoggedInHomePg;
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
