import React, { Component } from 'react'
// Local imports
// Elements
import {
    ImageDropZone,
    NextButton
} from '../elements/'


class ImagesForm extends Component {

    render = () => {
        return(
            <React.Fragment>
                <div>
                    <ImageDropZone
                        id='SET_IMAGES'
                        onDragOver={ (e) => {this.clearFileErrors(e)} }
                        onDrop={ (e) => {this.fileValidation(e)} }
                    />
                </div>
            </React.Fragment>
        )
    }


    clearFileErrors = (e) => {
        e.preventDefault()
        this.props.setInputErrors(false, e.target.id)
    }

    fileValidation = (e) => {
        e.preventDefault()

        // Raise error if user tries to upload any files but
        // jpg, jpeg or png and if the file size exceeds 2MB.
        const RegEx=/.*\.(jpg|jpeg|png)$/i
        let files = e.dataTransfer.files

        Object.values(files).forEach((file) => {
            if ((!(file.name.match(RegEx))) || (file.size > 2000000)) {
                this.props.setInputErrors(true, e.target.id)
            } else {
                this.props.prepareImageUpload(file)
            }
        })
    }

}


export default ImagesForm