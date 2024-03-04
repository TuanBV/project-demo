import React, { useState, useEffect } from "react";
import './ImageUpload.css'
import Modal from 'react-modal';

const BASE_URL = 'http://localhost:8000/'

function ImageUpload({ authToken, authTokenType, userId}) {
    const [caption, setCaption] = useState('')
    const [image, setImage] = useState('')
    const [openAdd, setOpenAdd] = useState(false)

    const customStyles = {
        content: {
          top: '50%',
          left: '50%',
          inset: '50% 40px 120px 50%',
          color: 'grey',
          transform: 'translate(-50%, -50%)',
        },
    };

    const handleChange = (e) => {
        if (e.target.files[0]) {
            setImage(e.target.files[0])
        }
    }

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

        fetch(BASE_URL + 'post/upload', requestOptions)
        .then(response => {
            if (response.ok) {
                return response.json()
            }
            throw response
        })
        .then(data => {
            setImage(null)
            createPost(data.filename)
        })
        .catch(err =>{
            console.log(err);
            alert(err)
        })
        .finally(() => {
            setCaption('')
            setImage(null)
        })
        setCaption('')
        setOpenAdd(false)
    }

    const createPost = (filename) => {
        const json_string = JSON.stringify({
            'caption': caption,
            'image_url': filename,
            'image_url_type': 'relative',
            'creator_id': userId,
        })
        const requestOptions = {
            method: 'POST',
            headers: new Headers({
                'Authorization': authTokenType + ' ' + authToken,
                'Content-Type': 'application/json',
            }),
            body: json_string,
        }

        fetch(BASE_URL + 'post', requestOptions)
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
            alert('Failed to add post.')
        })
    }
    return (
        <div className="image">
            <div className="image_upload">
                <button className="button_upload" onClick={() => setOpenAdd(true)}>Add post</button>

                <Modal
                    isOpen={openAdd}
                    style={customStyles}
                    onRequestClose={() => setOpenAdd(false)}
                >
                    <div className='modal_title'>Add post</div>
                    <form>
                    <div className='modal_label'>Caption: </div>
                    <input className='modal_input' type='text' value={caption} onChange={(e) => setCaption(e.target.value)} placeholder='Caption ...'/>
                    <div className='modal_label'>Choose image: </div>
                    <input id='fileImageUpload' type='file' onChange={handleChange}/>

                    <div className='modal_button'>
                        <button className='btn_add' onClick={create}>Add</button>
                        <button className='modal_buttonClose' onClick={() => setOpenAdd(false)}>Close</button>
                    </div>
                    </form>
                </Modal>
            </div>
        </div>
    )
}

export default ImageUpload