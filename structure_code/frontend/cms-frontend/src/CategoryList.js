import React, { useState, useEffect } from 'react';

function CategoryList() {
  const [categories, setCategories] = useState([]);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/categories/')
      .then((response) => response.json())
      .then((data) => {
        console.log("Fetched Categories:", data); // Log the fetched categories
        setCategories(data);
      })
      .catch((error) => console.error('Error fetching categories:', error));
  }, []);

  return (
    <div>
      <h2>Categories</h2>
      <ul className="category-list">
        {categories.length === 0 ? (
          <p>No categories available</p>
        ) : (
          categories.map((category) => (
            <li key={category.id}>{category.name}</li>
          ))
        )}
      </ul>
    </div>
  );
} 

export default CategoryList;
