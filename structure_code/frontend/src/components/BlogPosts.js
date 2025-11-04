import React, { useEffect, useState } from "react";
import axios from "axios";

const BlogPosts = () => {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    axios.get("http://localhost:8000/api/posts/") // Ensure this URL is correct
        .then(response => {
            setPosts(response.data);
        })
        .catch(error => {
            console.error("Error fetching posts:", error);
        });
}, []);


  return (
    <div className="min-h-screen bg-gray-100 flex justify-center">
      <div className="w-full max-w-2xl p-6">
        <h2 className="text-2xl font-semibold text-gray-700 mb-4">Blog Posts</h2>
        
        {posts.length === 0 ? (
          <p className="text-gray-600">Loading posts...</p>
        ) : (
          <div className="space-y-4">
            {posts.map((post) => (
              <div key={post.id} className="bg-white p-4 rounded-lg shadow-md hover:shadow-lg transition">
                <h3 className="text-xl font-semibold text-gray-900">{post.title}</h3>
                <p className="text-gray-600">{post.content.substring(0, 100)}...</p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default BlogPosts;
