import React, { Component } from 'react';

import axios from 'axios';


class AddImages extends Component {
    state = {
        image_file: null,
        artwork_object_id: this.props.location.state.artwork_object_id,
    }


    render() {
        return(
            <div>
                <p>Image</p>
                <input onChange={ this.selectedFile } type="file" />
                <br />
                <br />
                <button onClick={ this.uploadFile }>Save</button>
            </div>
        )
    }


    selectedFile = (event) => {
        this.setState({
            image_file: event.target.files[0]
        })
        console.log(event); //REMOVE
    }


    uploadFile = () => {
        const imageUploadForm = new FormData();
        imageUploadForm.set('title_id', this.state.artwork_object_id);
        imageUploadForm.append('images', this.state.image_file);
        axios.post('http://localhost:8000/artworks_images/', imageUploadForm, {headers: {'Content-Type': 'multipart/form-data'}})
        .then(response => {console.log(response)});
    }


}


export default AddImages;