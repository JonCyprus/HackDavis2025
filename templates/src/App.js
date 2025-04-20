import { useState } from "react";
// import logo from './logo.svg';
import './App.css';

function App() {
  const [state, setState] = useState('home')

  const CloudBtn = (props) => {
    return <button className="cloudBtn" onClick={props.goToNewTask}>New Task</button>
  }
  
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
          <div className="dialog"></div>
          <img src="images/tasky-01.svg" alt="tasky, a fluffy yellow blob with big eyes" />
        </div>
        <input name="talkToTasky" type="text" />
      </main>
    </div>);

    console.log(state.value);
    
  // if([logged in]){
  if(state === 'home'){
    return homePg;
  }
  else if(state === 'newTask'){
    return newTaskPg;
  }
  else{
    return logInPg;
  }
   //}

}

export default App;
