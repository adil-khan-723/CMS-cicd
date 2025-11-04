// src/pages/PostPage.js
// src/pages/PostPage.js

import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';

const PostPage = () => {
  const { id } = useParams();  // Get post ID from the URL
  const [post, setPost] = useState(null);

  useEffect(() => {
    const fetchPost = async () => {
      const response = await fetch(`http://localhost:8000/api/posts/${id}/`);
      const data = await response.json();
      setPost(data);
    };

    fetchPost();
  }, [id]);

  if (!post) return <p>Loading...</p>;

  return (
    <div className="post-page">
      <h1>{post.title}</h1>
      <p>{post.content}</p>
    </div>
  );
};

export default PostPage;

