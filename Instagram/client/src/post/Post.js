import React, { useEffect, useState } from "react";
import Modal from 'react-modal';
import './Post.css'

const BASE_URL = 'http://localhost:8000/'
const ws = new WebSocket('ws://localhost:8000/post/chat')

function Post({post, authToken, authTokenType, username}) {
    const [imageUrl, setImageUrl] = useState('')
    const [comments, setComments] = useState([])
    const [newComment, setNewComment] = useState('')
    const [openEdit, setOpenEdit] = useState(false)
    const [newCaption, setNewCaption] = useState('')
    const [image, setImage] = useState('')
    const [postId, setPostId] = useState('')

    const customStyleEdit = {
        content: {
          top: '50%',
          left: '50%',
          inset: '50% 40px 120px 50%',
          color: 'grey',
          transform: 'translate(-50%, -50%)',
        },
      };
    const deletePost = (postId) => {
        const requestOptions = {
            method: 'DELETE',
            headers: new Headers({
                'Authorization': authTokenType + ' ' + authToken,
            }),
        }

        fetch(BASE_URL + 'post/' + postId, requestOptions)
        .then(response => {
            if (response.ok) {
                window.location.reload()
            }
        })
        .catch(err => {
            console.log(err);
            alert('Failed to delete post')
        })
    }
    const handleChange = (e) => {
        if (e.target.files[0]) {
            setImage(e.target.files[0])
        }
    }
    const addComment = (event, postId, username) => {
        const json_string = JSON.stringify({
            'token': authToken,
            'post_id': postId,
            'username': username,
            'text': newComment
        })
        ws.send(json_string)
        setNewComment('')
        event.preventDefault()
    }

    ws.onmessage = function(event) {
        const dataConvert = JSON.parse(event.data)
        setComments(post.comment.push(dataConvert));
        console.log(dataConvert);
    };

    const create = (e) => {
        e?.preventDefault()

        const formData = new FormData()
        formData.append('image', image)

        const requestOptions = {
            method: 'POST',
            headers: new Headers({
                'Authorization': authTokenType + ' ' + authToken,
            }),
            body: formData,
        }
        if (!image) {
            updatePost(null);
        }
        else {
            fetch(BASE_URL + 'post/upload', requestOptions)
            .then(response => {
                if (response.ok) {
                    return response.json()
                }
                throw response
            })
            .then(data => {
                setImage(null)
                updatePost(data.filename)
            })
            .catch(err =>{
                console.log(err);
                alert(err)
            })
            .finally(() => {
                setNewCaption('')
                setImage(null)
            })
        }
        setNewCaption('')
        setOpenEdit(false)
    }

    const updatePost = (pathImage) => {
        console.log(newCaption);
        const json_string = JSON.stringify({
            'caption': newCaption,
            'image_url': pathImage,
        })
        const requestOptions = {
            method: 'PUT',
            headers: new Headers({
                'Authorization': authTokenType + ' ' + authToken,
                'Content-Type': 'application/json',
            }),
            body: json_string,
        }

        fetch(BASE_URL + 'post/' + postId, requestOptions)
        .then(response => {
            if (response.ok) {
                return response.json()
            }
            throw response
        })
        .then(data => {
            window.location.reload()
        })
        .catch(err => {
            console.log(err);
        });
    }

    useEffect(() => {
        if (post.image_url_type === "absolute") {
            setImageUrl(BASE_URL + post.image_url)
        }
        else {
            setImageUrl(BASE_URL + post.image_url)
        }
    }, [])

    useEffect(() => {
        setComments(post.comment)
    }, [comments])

    return (
        <div className='post'>
            <div className="post_header">
                <div className="post_avatar">
                    <img
                        className="post_avatar"
                        alt='Avatar'
                        src='https://static.vecteezy.com/system/resources/previews/009/292/244/original/default-avatar-icon-of-social-media-user-vector.jpg'
                    />
                </div>
                <div className="post_headerInfo">
                    <div className="post_username">{post.user.username}</div>
                    {
                        authToken && username === post.user.username
                        ? (
                            <div>
                                <button className='post_delete' onClick={() => {setOpenEdit(true);setPostId(post.id);setNewCaption(post.caption)}}>Edit</button>
                                <button className='post_delete' onClick={() => deletePost(post.id)}>Delete</button>
                            </div>
                        )
                        : ('')
                    }
                </div>
            </div>

            <img
                className="post_image"
                src={imageUrl}
                alt={post.caption}
            />
            {
                <h5 className="post_caption">{post.caption}</h5>
            }
            
            {
                Object.keys(comments).length
                ? (
                    <div className="post_comment">
                        <div>
                            {
                                Object.keys(comments).length ? ('Comment:') : ('')
                            }
                        </div>
                        <p >
                            {
                                comments.map((comment) =>(
                                    <div>
                                        <strong>{comment.username}: </strong> {comment.text}
                                    </div>
                                ))
                            }
                        </p>
                    </div>
                )
                : null
            }
            {
                authToken && (
                    <form className="comment_post">
                        <input
                            className="input_comment" type='text' placeholder="Add a comment ..." value={newComment} onChange={(e) => setNewComment(e.target.value)}
                        />
                        <button disabled={!newComment}
                            className="button_comment" onClick={(event) => addComment(event, post.id, username)}>Add</button>
                    </form>
                )
            }
          <Modal
            isOpen={openEdit}
            style={customStyleEdit}
            contentLabel="Example Modal"
            onRequestClose={() => setOpenEdit(false)}
          >
            <div className='modal_title'>Login</div>
            <form>
                <div className='modal_label'>Caption: </div>
                <input className='modal_input' type='text' value={newCaption} onChange={(e) => setNewCaption(e.target.value)} placeholder='Caption'/>
                <div className='modal_label'>Choose image: </div>
                <input id='fileImageUpload' type='file' onChange={handleChange}/>

                <div className='modal_button'>
                    <button className='btn_add' onClick={(e) => create(e)}>Update</button>
                    <button className='modal_buttonClose' onClick={() => setOpenEdit(false)}>Close</button>
                </div>
            </form>
          </Modal>

        </div>
    )
}

export default Post