import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

import BlogPostList from './BlogPostList';
import BlogPostForm from './BlogPostForm';

function App() {
  return (
    <Router>
      <div>
        <Routes>
          <Route exact path="/posts" component={BlogPostList} />
          <Route path="/create-post" component={BlogPostForm} />
          <Route path="/edit-post/:id" component={BlogPostForm} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
