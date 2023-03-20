// SearchBar.js

import React, { useState } from 'react';

function SearchBar() {
  const [searchQuery, setSearchQuery] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    const response = await fetch('/search_tweets', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ search_query: searchQuery })
    });
    const searchResults = await response.json();
    // render the search results in the component
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="text" value={searchQuery} onChange={(e) => setSearchQuery(e.target.value)} />
      <button type="submit">Search</button>
    </form>
  );
}