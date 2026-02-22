import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { postsAPI } from '../api/axios';
import PostCard from '../components/PostCard';
import './Search.css';

const Search = () => {
  const navigate = useNavigate();
  
  const [searchParams, setSearchParams] = useState({
    query: '',
    category: '',
    location: '',
    date_from: '',
    date_to: ''
  });

  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchPosts = async () => {
      setLoading(true);
      try {
        const params = new URLSearchParams();
        if (searchParams.query) params.append('query', searchParams.query);
        if (searchParams.category) params.append('category', searchParams.category);
        if (searchParams.location) params.append('location', searchParams.location);
        if (searchParams.date_from) params.append('date_from', searchParams.date_from);
        if (searchParams.date_to) params.append('date_to', searchParams.date_to);

        const response = await postsAPI.search(Object.fromEntries(params));
        setPosts(response.data);
      } catch (err) {
        setError('Failed to search posts');
      } finally {
        setLoading(false);
      }
    };

    fetchPosts();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setSearchParams(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSearch = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const params = {};
      if (searchParams.query) params.query = searchParams.query;
      if (searchParams.category) params.category = searchParams.category;
      if (searchParams.location) params.location = searchParams.location;
      if (searchParams.date_from) params.date_from = searchParams.date_from;
      if (searchParams.date_to) params.date_to = searchParams.date_to;

      const response = await postsAPI.search(params);
      setPosts(response.data);
    } catch (err) {
      setError('Failed to search posts');
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setSearchParams({
      query: '',
      category: '',
      location: '',
      date_from: '',
      date_to: ''
    });
  };

  return (
    <div className="search-container">
      <div className="search-header">
        <h1>Search Lost & Found Items</h1>
        <p>Find items that have been lost or found</p>
      </div>

      <div className="search-filters">
        <form onSubmit={handleSearch} className="filter-form">
          <div className="filter-row">
            <div className="form-group">
              <label htmlFor="query">Search Query</label>
              <input
                type="text"
                id="query"
                name="query"
                value={searchParams.query}
                onChange={handleChange}
                placeholder="Search by title or description"
              />
            </div>

            <div className="form-group">
              <label htmlFor="category">Category</label>
              <select
                id="category"
                name="category"
                value={searchParams.category}
                onChange={handleChange}
              >
                <option value="">All Categories</option>
                <option value="lost">Lost Items</option>
                <option value="found">Found Items</option>
              </select>
            </div>
          </div>

          <div className="filter-row">
            <div className="form-group">
              <label htmlFor="location">Location</label>
              <input
                type="text"
                id="location"
                name="location"
                value={searchParams.location}
                onChange={handleChange}
                placeholder="City or area"
              />
            </div>

            <div className="form-group">
              <label htmlFor="date_from">Date From</label>
              <input
                type="date"
                id="date_from"
                name="date_from"
                value={searchParams.date_from}
                onChange={handleChange}
              />
            </div>

            <div className="form-group">
              <label htmlFor="date_to">Date To</label>
              <input
                type="date"
                id="date_to"
                name="date_to"
                value={searchParams.date_to}
                onChange={handleChange}
              />
            </div>
          </div>

          <div className="filter-actions">
            <button type="submit" disabled={loading} className="search-btn">
              {loading ? 'Searching...' : 'Search'}
            </button>
            <button type="button" onClick={handleClear} className="clear-btn">
              Clear Filters
            </button>
          </div>
        </form>
      </div>

      <div className="search-results">
        {error && <div className="error-message">{error}</div>}
        
        {loading ? (
          <div className="loading">Searching...</div>
        ) : (
          <>
            <div className="results-header">
              <h3>Results ({posts.length} items found)</h3>
            </div>
            
            {posts.length === 0 ? (
              <div className="no-results">
                <p>No items found matching your search criteria.</p>
                <button 
                  onClick={() => navigate('/create-post')} 
                  className="create-post-btn"
                >
                  Create New Post
                </button>
              </div>
            ) : (
              <div className="posts-grid">
                {posts.map(post => (
                  <PostCard key={post.id} post={post} />
                ))}
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default Search;
