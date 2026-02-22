import React from 'react';
import { useNavigate } from 'react-router-dom';
import './PostCard.css';

const PostCard = ({ post }) => {
  const navigate = useNavigate();

  const handleClick = () => {
    navigate(`/posts/${post.id}`);
  };

  const formatDate = (dateString) => {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
  };

  return (
    <div className="post-card" onClick={handleClick}>
      {post.image_url && (
        <div className="post-image">
          <img 
            src={post.image_url} 
            alt={post.title}
            onError={(e) => {
              e.target.style.display = 'none';
            }}
          />
        </div>
      )}
      
      <div className="post-content">
        <div className="post-header">
          <span className={`category-badge ${post.category}`}>
            {post.category === 'lost' ? 'LOST' : 'FOUND'}
          </span>
          <span className="post-date">{formatDate(post.date)}</span>
        </div>
        
        <h3 className="post-title">{post.title}</h3>
        
        <p className="post-description">
          {post.description.length > 150 
            ? `${post.description.substring(0, 150)}...` 
            : post.description}
        </p>
        
        <div className="post-footer">
          <div className="post-location">
            📍 {post.location}
          </div>
          <div className="post-contact">
            📧 Contact Available
          </div>
        </div>
      </div>
    </div>
  );
};

export default PostCard;
