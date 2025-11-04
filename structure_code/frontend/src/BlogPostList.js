import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

function BlogPostList() {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/posts/')
      .then((response) => response.json())
      .then((data) => setPosts(data.results))  // Adjusted to get paginated results
      .catch((error) => console.error('Error fetching posts:', error));
  }, []);

  return (
    <div>
      <h2>Blog Posts</h2>
      <ul className="post-list">
        {posts.map((post) => (
          <li key={post.id}>
            <h3>{post.title}</h3>
            <p>{post.content}</p>
            <p><strong>Category:</strong> {post.category.name}</p>
            <Link to={`/edit-post/${post.id}`}>Edit</Link>
          </li>
        ))}
      </ul>
      <Link to="/create-post">Create a New Post</Link>
    </div>
  );
}

export default BlogPostList;
