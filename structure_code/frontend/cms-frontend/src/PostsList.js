// src/PostsList.js
import React, { useEffect, useState } from 'react';

function PostsList() {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/posts/')
      .then((response) => response.json())
      .then((data) => setPosts(data))
      .catch((error) => console.error('Error fetching posts:', error));
  }, []);

  return (
    <div>
      <h2>Posts List</h2>
      <ul>
        {posts.map((post) => (
          <li key={post.id}>
            <h3>{post.title}</h3>
            <p>{post.content}</p>
            <a href={`/posts/${post.id}/edit`}>Edit</a>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default PostsList;
