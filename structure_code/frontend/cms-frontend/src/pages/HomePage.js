// src/pages/HomePage.js

import React, { useEffect, useState } from 'react';
import PostCard from '../components/PostCard';  // Assuming you have a PostCard component to display posts

const HomePage = () => {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);  // To track loading state
  const [error, setError] = useState(null);  // To track errors

  useEffect(() => {
    // Fetch posts from the backend API
    const fetchPosts = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/posts/');
        if (!response.ok) {
          throw new Error('Failed to fetch posts');
        }
        const data = await response.json();
        setPosts(data);
      } catch (error) {
        setError(error.message);  // Capture error message
      } finally {
        setLoading(false);  // Stop loading spinner after data is fetched
      }
    };

    fetchPosts();
  }, []);  // Empty dependency array means it will run only once after initial render

  if (loading) return <p>Loading posts...</p>;  // Show loading state
  if (error) return <p>Error: {error}</p>;  // Show error message if fetching fails

  return (
    <div className="home-page">
      <h1>Blog Posts</h1>
      <div className="post-list">
        {posts.length === 0 ? (
          <p>No posts available.</p>  // Show message if no posts are available
        ) : (
          posts.map(post => (
            <PostCard key={post.id} post={post} />  // Pass each post to PostCard component
          ))
        )}
      </div>
    </div>
  );
};

export default HomePage;

