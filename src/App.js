import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, Link, useNavigate } from 'react-router-dom';
import { isAuthenticated } from './utils/auth';
import CreatePost from './pages/CreatePost';
import EditPost from './pages/EditPost';
import Search from './pages/Search';
import './App.css';

const Home = () => {
  const navigate = useNavigate();
  
  return (
    <div className="home">
      <h1>Lost & Found Platform</h1>
      <p>Find your lost items or report found items</p>
      <div className="home-actions">
        <button onClick={() => navigate('/search')} className="btn-primary">
          Search Items
        </button>
        <button onClick={() => navigate('/create-post')} className="btn-secondary">
          Post Item
        </button>
      </div>
    </div>
  );
};

const Login = () => {
  return (
    <div className="login">
      <h2>Login</h2>
      <p>Login functionality to be implemented</p>
    </div>
  );
};

const ProtectedRoute = ({ children }) => {
  return isAuthenticated() ? children : <Navigate to="/login" />;
};

function App() {
  return (
    <Router>
      <div className="App">
        <nav className="navbar">
          <div className="nav-brand">
            <h2>Lost & Found</h2>
          </div>
          <div className="nav-links">
            <Link to="/">Home</Link>
            <Link to="/search">Search</Link>
            <Link to="/create-post">Post Item</Link>
            {isAuthenticated() ? (
              <Link to="/logout">Logout</Link>
            ) : (
              <Link to="/login">Login</Link>
            )}
          </div>
        </nav>

        <main className="main-content">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/search" element={<Search />} />
            <Route 
              path="/create-post" 
              element={
                <ProtectedRoute>
                  <CreatePost />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/edit-post/:id" 
              element={
                <ProtectedRoute>
                  <EditPost />
                </ProtectedRoute>
              } 
            />
            <Route path="*" element={<Navigate to="/" />} />
          </Routes>
        </main>

        <footer className="footer">
          <p>&copy; 2024 Lost & Found Platform. All rights reserved.</p>
        </footer>
      </div>
    </Router>
  );
}

export default App;
