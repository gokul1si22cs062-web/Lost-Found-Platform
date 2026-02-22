# Lost & Found Platform

A comprehensive platform for users to post and search for lost and found items.

## Features

- **User Authentication**: JWT-based authentication system
- **Post Management**: Create, read, update, and delete posts
- **Search & Filter**: Advanced search with multiple filters
- **Ownership Logic**: Only post owners can edit/delete their posts
- **Contact System**: Built-in messaging between users
- **Responsive Design**: Mobile-friendly interface

## Tech Stack

### Frontend (Member 2 - Frontend Logic & Integration)
- React 18
- React Router for navigation
- Axios for API integration
- CSS for styling
- JWT token management

### Backend
- FastAPI
- JWT Authentication
- MongoDB for data storage

## Project Structure

```
lost-found-frontend/
├── public/
│   └── index.html
├── src/
│   ├── api/
│   │   └── axios.js          # API configuration and endpoints
│   ├── pages/
│   │   ├── CreatePost.jsx    # Create new post form
│   │   ├── EditPost.jsx      # Edit existing post
│   │   └── Search.jsx        # Search and filter interface
│   ├── components/
│   │   └── PostCard.jsx      # Post display component
│   ├── utils/
│   │   └── auth.js           # Authentication utilities
│   ├── App.js                # Main application component
│   ├── App.css               # Global styles
│   └── main.jsx              # Application entry point
├── package.json
└── README.md
```

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

## API Integration

The frontend integrates with a FastAPI backend running on `http://localhost:8000`. Key API endpoints:

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/profile` - Get user profile

### Posts
- `GET /api/posts` - Get all posts
- `GET /api/posts/:id` - Get specific post
- `POST /api/posts` - Create new post
- `PUT /api/posts/:id` - Update post
- `DELETE /api/posts/:id` - Delete post
- `GET /api/posts/search` - Search posts

### Contact
- `POST /api/contact/send` - Send message
- `GET /api/contact/messages` - Get messages

## Authentication Flow

1. JWT tokens are stored in localStorage
2. Automatic token injection in API requests
3. Token validation and expiration handling
4. Protected routes for authenticated users

## Key Components

### API Configuration (`src/api/axios.js`)
- Centralized API configuration
- Request/response interceptors
- Automatic token management
- Error handling

### Authentication Utils (`src/utils/auth.js`)
- Token validation
- User session management
- Protected route utilities

### Forms
- Create post with validation
- Edit post with ownership check
- Search with multiple filters

## Development Notes

- All API calls are handled through centralized axios instance
- JWT tokens are automatically attached to requests
- Error handling includes user-friendly messages
- Responsive design works on mobile and desktop
- Component-based architecture for maintainability
