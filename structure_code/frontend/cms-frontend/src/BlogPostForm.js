import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';

function BlogPostForm() {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [category, setCategory] = useState('');
  const [categories, setCategories] = useState([]);
  const [isEditing, setIsEditing] = useState(false);
  const { id } = useParams();
  const navigate = useNavigate();

  useEffect(() => {
    // Fetch categories for select input
    fetch('http://127.0.0.1:8000/api/categories/')
      .then((response) => response.json())
      .then((data) => setCategories(data))
      .catch((error) => console.error('Error fetching categories:', error));

    if (id) {
      // Fetch the post to edit
      setIsEditing(true);
      fetch(`http://127.0.0.1:8000/api/posts/${id}/`)
        .then((response) => response.json())
        .then((data) => {
          setTitle(data.title);
          setContent(data.content);
          setCategory(data.category.id);
        })
        .catch((error) => console.error('Error fetching post:', error));
    }
  }, [id]);

  const handleSubmit = (e) => {
    e.preventDefault();
    const method = isEditing ? 'PUT' : 'POST';
    const url = isEditing
      ? `http://127.0.0.1:8000/api/posts/${id}/`
      : 'http://127.0.0.1:8000/api/posts/';

    const postData = { title, content, category };

    fetch(url, {
      method,
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(postData),
    })
      .then(() => navigate('/posts')) // Redirect after submit
      .catch((error) => console.error('Error saving post:', error));
  };

  const handleDelete = () => {
    fetch(`http://127.0.0.1:8000/api/posts/${id}/`, {
      method: 'DELETE',
    })
      .then(() => navigate('/posts')) // Redirect after delete
      .catch((error) => console.error('Error deleting post:', error));
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>{isEditing ? 'Edit Post' : 'Create Post'}</h2>
      <div>
        <label>Title</label>
        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
        />
      </div>
      <div>
        <label>Content</label>
        <textarea
          value={content}
          onChange={(e) => setContent(e.target.value)}
          required
        />
      </div>
      <div>
        <label>Category</label>
        <select
          value={category}
          onChange={(e) => setCategory(e.target.value)}
          required
        >
          {categories.map((category) => (
            <option key={category.id} value={category.id}>
              {category.name}
            </option>
          ))}
        </select>
      </div>
      <button type="submit">{isEditing ? 'Update Post' : 'Create Post'}</button>
      {isEditing && (
        <button type="button" onClick={handleDelete}>
          Delete Post
        </button>
      )}
    </form>
  );
}

export default BlogPostForm;
