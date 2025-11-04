import React, { useState, useEffect } from 'react';
import BlogList from '../components/BlogList';

const HomePage = () => {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    // Fetch blog posts from your API or local data
    const fetchPosts = async () => {
      const response = await fetch('http://localhost:8000/api/posts');
      const data = await response.json();
      setPosts(data);
    };

    fetchPosts();
  }, []);

  return (
    <div>
      <h1>Home Page</h1>
      <BlogList posts={posts} />
    </div>
  );
};

export default HomePage;
