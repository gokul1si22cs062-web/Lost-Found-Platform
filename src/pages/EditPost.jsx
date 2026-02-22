import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { postsAPI } from '../api/axios';
import './EditPost.css';

const EditPost = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    category: 'lost',
    location: '',
    date: '',
    contact_info: '',
    image_url: ''
  });

  const [loading, setLoading] = useState(false);
  const [fetchLoading, setFetchLoading] = useState(true);
  const [error, setError] = useState('');
  const [notFound, setNotFound] = useState(false);

  useEffect(() => {
    const fetchPost = async () => {
      try {
        const response = await postsAPI.getById(id);
        setFormData(response.data);
      } catch (err) {
        if (err.response?.status === 404) {
          setNotFound(true);
        } else {
          setError('Failed to fetch post details');
        }
      } finally {
        setFetchLoading(false);
      }
    };

    fetchPost();
  }, [id]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      await postsAPI.update(id, formData);
      navigate(`/posts/${id}`);
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to update post');
    } finally {
      setLoading(false);
    }
  };

  if (fetchLoading) {
    return <div className="loading">Loading post details...</div>;
  }

  if (notFound) {
    return (
      <div className="not-found">
        <h2>Post Not Found</h2>
        <p>The post you're trying to edit doesn't exist.</p>
        <button onClick={() => navigate('/')} className="back-btn">
          Back to Home
        </button>
      </div>
    );
  }

  return (
    <div className="edit-post-container">
      <div className="edit-post-form">
        <h2>Edit Post</h2>
        {error && <div className="error-message">{error}</div>}
        
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="title">Title *</label>
            <input
              type="text"
              id="title"
              name="title"
              value={formData.title}
              onChange={handleChange}
              required
              placeholder="Brief description of the item"
            />
          </div>

          <div className="form-group">
            <label htmlFor="category">Category *</label>
            <select
              id="category"
              name="category"
              value={formData.category}
              onChange={handleChange}
              required
            >
              <option value="lost">Lost Item</option>
              <option value="found">Found Item</option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="description">Description *</label>
            <textarea
              id="description"
              name="description"
              value={formData.description}
              onChange={handleChange}
              required
              rows="4"
              placeholder="Detailed description of the item"
            />
          </div>

          <div className="form-group">
            <label htmlFor="location">Location *</label>
            <input
              type="text"
              id="location"
              name="location"
              value={formData.location}
              onChange={handleChange}
              required
              placeholder="Where the item was lost/found"
            />
          </div>

          <div className="form-group">
            <label htmlFor="date">Date *</label>
            <input
              type="date"
              id="date"
              name="date"
              value={formData.date}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="contact_info">Contact Information *</label>
            <input
              type="text"
              id="contact_info"
              name="contact_info"
              value={formData.contact_info}
              onChange={handleChange}
              required
              placeholder="Email or phone number"
            />
          </div>

          <div className="form-group">
            <label htmlFor="image_url">Image URL (optional)</label>
            <input
              type="url"
              id="image_url"
              name="image_url"
              value={formData.image_url}
              onChange={handleChange}
              placeholder="https://example.com/image.jpg"
            />
          </div>

          <div className="form-actions">
            <button type="submit" disabled={loading} className="submit-btn">
              {loading ? 'Updating...' : 'Update Post'}
            </button>
            <button 
              type="button" 
              onClick={() => navigate(`/posts/${id}`)} 
              className="cancel-btn"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default EditPost;
