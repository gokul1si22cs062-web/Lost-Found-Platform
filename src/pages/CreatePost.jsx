import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { postsAPI } from '../api/axios';
import './CreatePost.css';

const CreatePost = () => {
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
  const [error, setError] = useState('');
  const navigate = useNavigate();

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
      const response = await postsAPI.create(formData);
      navigate(`/posts/${response.data.id}`);
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to create post');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="create-post-container">
      <div className="create-post-form">
        <h2>Create New Post</h2>
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

          <button type="submit" disabled={loading} className="submit-btn">
            {loading ? 'Creating...' : 'Create Post'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default CreatePost;
