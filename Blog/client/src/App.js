import './App.css';
import React, { useEffect, useState } from 'react';
import Post from './post/Post';
import NewPost from './post/NewPost';

const BASE_URL = 'http://localhost:8000/'

function App() {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    fetch(BASE_URL + 'blog/all')
    .then(response => {
      const json = response.json()
      console.log(json);
      if (response.ok) {
        return json
      }
      throw response
    })
    .then(data => {
      return data.reverse();
    })
    .then(data => {
      setPosts(data)
    })
    .catch(error => {
      console.log(error);
      alert(error)
    })
  }, [])
  return (
    <div className="App">
      <div className='blog_title'>Project Blog</div>
      <div className='app_post'>
        {
          posts.map(post => (
            <Post post={post}/>
          ))
        }
      </div>

      <div className='newpost'>
          Add new post
          <NewPost/>
      </div>
    </div>
  );
}

export default App;
