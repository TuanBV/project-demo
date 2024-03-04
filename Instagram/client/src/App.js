import React, { useEffect, useState } from 'react';
import './App.css';
import Post from './post/Post';
import ImageUpload from './imageUpload/ImageUpload';
import Modal from 'react-modal';

const BASE_URL = 'http://localhost:8000/'

function App() {

  const [posts, setPosts] = useState([])
  const [openSignIn, setOpenSignIn] = useState(false)
  const [openSignUp, setOpenSignUp] = useState(false)
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [authToken, setAuthToken] = useState(null)
  const [authTokenType, setAuthTokenType] = useState(null)
  const [userId, setUserId] = useState('')
  const [fullname, setFullname] = useState('')
  const [email, setEmail] = useState('')

  useEffect(() => {
    setAuthToken(window.localStorage.getItem('authToken'))
    setAuthTokenType(window.localStorage.getItem('authTokenType'))
    setUsername(window.localStorage.getItem('username'))
    setUserId(window.localStorage.getItem('userId'))
  }, [])

  useEffect(() => {
    authToken
      ? window.localStorage.setItem('authToken', authToken)
      : window.localStorage.removeItem('authToken')
    authTokenType
      ? window.localStorage.setItem('authTokenType', authTokenType)
      : window.localStorage.removeItem('authTokenType')
    username
      ? window.localStorage.setItem('username', username)
      : window.localStorage.removeItem('username')
    userId
      ? window.localStorage.setItem('userId', userId)
      : window.localStorage.removeItem('userId')
  }, [authToken, authTokenType, username, userId])

  const customStylesSingIn = {
    content: {
      top: '50%',
      left: '50%',
      inset: '50% 40px 120px 50%',
      color: 'grey',
      transform: 'translate(-50%, -50%)',
    },
  };

  const customStylesSingUp = {
    content: {
      top: '50%',
      left: '50%',
      height: '420px',
      inset: '50% 40px 120px 50%',
      color: 'grey',
      transform: 'translate(-50%, -50%)',
    },
  };

  const signIn = (event) => {
    event?.preventDefault();

    const formData = new FormData();
    formData.append('username', username)
    formData.append('password', password)

    const requestOptions = {
      method: 'POST',
      body: formData,
    }

    fetch(BASE_URL + 'login', requestOptions)
    .then(response => {
      if (response.ok) {
        return response.json()
      }
      throw response
    })
    .then(data => {
      setAuthToken(data.access_token)
      setAuthTokenType(data.token_type)
      setUserId(data.user_id)
      setUsername(data.username)
    })
    .catch(err => {
      console.log(err);
      alert('Username or password incorrect.')
    })

    setOpenSignIn(false)
  }

  const signUp = (event) => {
    event?.preventDefault()

    let json_string = JSON.stringify({
      username: username,
      email: email,
      full_name: fullname,
      password: password
    })

    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: json_string,
    }
    fetch(BASE_URL + 'user', requestOptions)
    .then(response => {
      if (response.ok) {
        return response.json()
      }
      throw response
    })
    .then(data => {
      signIn()
    })
    .catch(err => {
      console.log(err)
      alert(err)
    })

    setOpenSignUp(false)
  }
  const logOut = (event) => {
    setAuthToken(null)
    setAuthTokenType(null)
    setUserId('')
    setUsername('')
  }

  useEffect(() => {
    fetch(BASE_URL + 'post/all')
    .then(response => {
      if (response.ok) {
        return response.json()
      }
      throw response
    })
    .then(data => {
      setPosts(data)
    })
    .catch(err => {
      console.log(err);
      alert(err)
    })
  }, [])

  return (
    <div className="app_post">
      <div className="app_header">
          <img className="app_headerImage"
              src="//upload.wikimedia.org/wikipedia/commons/e/e7/Instagram_logo_2016.svg"
              alt="Logo"
          />
          {/* Modal sign in */}
          <Modal
            isOpen={openSignIn}
            style={customStylesSingIn}
            contentLabel="Example Modal"
            onRequestClose={() => setOpenSignIn(false)}
          >
            <div className='modal_title'>Login</div>
            <form>
              <div className='modal_label'>Username: </div>
              <input className='modal_input' type='text' value={username} onChange={(e) => setUsername(e.target.value)} placeholder='Username'/>
              <div className='modal_label'>Password: </div>
              <input className='modal_input'type='password' value={password} onChange={(e) => setPassword(e.target.value)} placeholder='************'/>
              <div className='modal_button'>
                <button className='modal_buttonLogin' onClick={signIn}>Login</button>
                <button className='modal_buttonClose' onClick={() => setOpenSignIn(false)}>Close</button>
              </div>
            </form>
          </Modal>
          {/* Modal sign up */}
          <Modal
            isOpen={openSignUp}
            style={customStylesSingUp}
            contentLabel="Example Modal"
            onRequestClose={() => setOpenSignIn(false)}
          >
            <div className='modal_title'>Sign Up</div>
            <form>
              <div className='modal_label'>Username: </div>
              <input className='modal_input' type='text' value={username} placeholder='Username' onChange={(e) => setUsername(e.target.value)}/>
              <div className='modal_label'>Email: </div>
              <input className='modal_input' type='text' value={email} placeholder='Email' onChange={(e) => setEmail(e.target.value)}/>
              <div className='modal_label'>Fullname: </div>
              <input className='modal_input' type='text' value={fullname} placeholder='Fullname' onChange={(e) => setFullname(e.target.value)}/>
              <div className='modal_label'>Password: </div>
              <input className='modal_input'type='password' value={password} placeholder='********' onChange={(e) => setPassword(e.target.value)}/>
              <div className='modal_button'>
                <button className='modal_buttonLogin' onClick={signUp}>Sign Up</button>
                <button className='modal_buttonClose' onClick={() => setOpenSignIn(false)}>Close</button>
              </div>
            </form>
          </Modal>

          <div className='app_headerButton'>
            {
              authToken === null
              ? (
                <div>
                  <button onClick={() => {setPassword(''); setUsername('');setOpenSignIn(true); setOpenSignUp(false)}}>LOGIN</button>
                  <button onClick={() => {setPassword(''); setUsername('');setEmail(''); setFullname('');setOpenSignIn(false); setOpenSignUp(true)}}>SIGN UP</button>
                </div>
              )
              : (
                <button onClick={() => logOut()}>LOG OUT</button>
              )
            }

          </div>
      </div>
      {
        authToken
        ? (<ImageUpload authToken={authToken} authTokenType={authTokenType} userId={userId}/>)
        : null
      }
      {
        posts.map(post => (
          <Post post={post} authToken={authToken} authTokenType={authTokenType} username={username}/>
        ))
      }
    </div>
  )
}

export default App
