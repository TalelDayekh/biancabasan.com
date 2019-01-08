import React, { Component } from 'react';
import axios from 'axios';
import './Admin.css';
import {
    AdminContentWrapper,
    ImageDropZone
} from '../elements/';


class AddImages extends Component {

    state = {
        fileDropHover: false,
        // Upload status
        failedUploads: []
    }

    render = () => {
        return(
            <AdminContentWrapper>
                <div className = "top-input-flex-container">
                    <ImageDropZone
                        onDragOver = { this.fileDropHover }
                        onDragLeave = { this.fileDropHover }
                        onDrop = { this.uploadFiles }
                        fileDropHover = { this.state.fileDropHover ? true : undefined }
                    >
                    </ImageDropZone>
                </div>
            </AdminContentWrapper>
        )
    }


    fileDropHover = (event) => {
        if (event.type === 'dragover') {
            this.setState({
                fileDropHover: true
            });
        };
        if (event.type === 'dragleave') {
            this.setState({
                fileDropHover: false
            });
        };
        event.preventDefault();
    }

    uploadFiles = (event) => {
        Object.keys(event.dataTransfer.files).map((image) => {
            let image_file = event.dataTransfer.files[image]
            let failedUpload = this.state.failedUploads.slice();
            const imageUploadForm = new FormData();

            // Validate image file size and upload
            // only if image is smaller than 2MB
            if (image_file.size > 600000) {
                failedUpload.push(image_file.name);
                this.setState({
                    fileDropHover: false,
                    failedUploads: failedUpload
                })
            } else {
                imageUploadForm.set('title', 41) // !! REMOVE HARD CODED ID !!
                imageUploadForm.append('image', image_file)

                axios.post('http://localhost:8000/admin_artworks/add_images/', imageUploadForm, {headers: {'Content-Type': 'multipart/form-data'}})
            }
        });
        event.preventDefault();
    }

}


export default AddImages;