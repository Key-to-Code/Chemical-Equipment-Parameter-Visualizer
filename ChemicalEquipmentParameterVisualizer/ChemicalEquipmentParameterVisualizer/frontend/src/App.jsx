import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import Upload from './components/Upload'
import DatasetList from './components/DatasetList'
import DatasetDetail from './components/DatasetDetail'
import './App.css'

function App() {
  return (
    <Router>
      <div className="app">
        <header className="app-header">
          <h1>Chemical Equipment Parameter Visualizer</h1>
          <nav>
            <Link to="/">Upload Data</Link>
            <Link to="/datasets">History</Link>
          </nav>
        </header>
        <main className="app-main">
          <Routes>
            <Route path="/" element={<Upload />} />
            <Route path="/datasets" element={<DatasetList />} />
            <Route path="/datasets/:id" element={<DatasetDetail />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App
