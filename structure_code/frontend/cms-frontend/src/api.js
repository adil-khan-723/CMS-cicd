// frontend/src/api.js
import axios from "axios";

// API URL for fetching posts and categories
const API_URL = "http://127.0.0.1:8000/api";

// Get posts
export const getPosts = async () => {
  try {
    const response = await axios.get(`${API_URL}/posts/`);
    return response.data;
  } catch (error) {
    console.error("There was an error fetching posts:", error);
    return [];
  }
};

// Get categories
export const getCategories = async () => {
  try {
    const response = await axios.get(`${API_URL}/categories/`);
    return response.data;
  } catch (error) {
    console.error("There was an error fetching categories:", error);
    return [];
  }
};
