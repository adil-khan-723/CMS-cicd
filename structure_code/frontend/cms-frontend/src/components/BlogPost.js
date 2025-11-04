// src/components/BlogPost.js

import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom"; // To get the dynamic post ID from the URL
import axios from "axios";

const BlogPost = () => {
  const [post, setPost] = useState(null);
  const [loading, setLoading] = useState(true);
  const { id } = useParams(); // Get the post ID from the URL

  useEffect(() => {
    // Fetch the post data from the backend
    const fetchPost = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/api/posts/${id}/`);
        setPost(response.data);
      } catch (error) {
        console.error("Error fetching the post data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchPost();
  }, [id]);

  // Loading state
  if (loading) {
    return <div>Loading...</div>;
  }

  // Render post details
  return (
    <div className="blog-post">
      {post ? (
        <>
          <h1>{post.title}</h1>
          <p>{post.content}</p>
          <p><strong>Published:</strong> {new Date(post.created_at).toLocaleDateString()}</p>
          {/* You can add more fields based on your post model */}
        </>
      ) : (
        <p>Post not found</p>
      )}
    </div>
  );
};

export default BlogPost;
