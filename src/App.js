import logo from './logo.svg';
import './App.css';
import SongList from './Components/SongList/SongList.js'

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>
          Hamilton Lyric Extravaganza
        </h1>
        <SongList/>

      </header>
    </div>
  );
}

export default App;
