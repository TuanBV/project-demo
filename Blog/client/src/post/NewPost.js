import React, { useState} from "react";
import './NewPost.css'

const BASE_URL = 'http://localhost:8000/'

function NewPost(){
    const [image, setImage] = useState(null)
    const [creator, setCreator] = useState('')
    const [title, setTitle] = useState('')
    const [text, setText] = useState('')

    const handleImageUpload = (e) =>{
        console.log(e);
        if (e.target.files[0]) {
            setImage(e.target.files[0])
        }
    }

    const handleCreate = (e) =>{
        e?.preventDefault()

        const formData = new FormData()
        formData.append('image', image)

        const requestOptions = {
            method: 'POST',
            body: formData
        }

        fetch(BASE_URL + 'blog/upload-image', requestOptions)
        .then(response => {
            if (response.ok) {
                return response.json()
            }
            throw response
        })
        .then(data => {
            createPost(data.filename)
        })
        .catch(err => {
            console.log(err);
        })
        .finally(() => {
            setImage(null)
            document.getElementById('fileInput').value =null
        })
    }

    const createPost = (pathImage) => {
        const json_string = JSON.stringify({
            'image_url': pathImage,
            'title': title,
            'content': text,
            'creator': creator,
        })

        const requestOptions = {
            method: 'POST',
            headers: new Headers({
                'Content-Type': 'application/json'
            }),
            body: json_string,
        }

        fetch(BASE_URL + 'blog', requestOptions)
        .then(response => {
            if (response.ok) {
                return response.json()
            }
            throw response
        })
        .then(data => {
            window.location.reload()
            window.scrollTo(0, 0)
        })
        .catch(err => {
            console.log(err);
        })
    }

    return (
        <div className='newpost_content'>
            <div className="newpost_image">
                <input type="file" id="fileInput" onChange={handleImageUpload}/>
            </div>
            <div className="newpost_creator">
                <input className="newpost_creator" type="text" id="creator_input"
                    placeholder="Creator" value={creator}
                    onChange={(event) => setCreator(event.target.value)}
                />
            </div>
            <div className="newpost_title">
                <input className="newpost_title" type="text" id="title_input"
                    placeholder="Title" value={title}
                    onChange={(event) => setTitle(event.target.value)}
                />
            </div>
            <div className="newpost_text">
                <textarea className="newpost_text" type="text" id="text_input"
                    placeholder="Text" value={text} rows='10'
                    onChange={(event) => setText(event.target.value)}
                />
            </div>
            <div>
                <button className="newpost_button" onClick={handleCreate}>Add</button>
            </div>
        </div>
    )
}

export default NewPost
