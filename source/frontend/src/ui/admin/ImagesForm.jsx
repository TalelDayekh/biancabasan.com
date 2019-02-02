import React, { Component } from 'react';
// Local imports
import '../../App.css';
import {
    ImageDropZone,
    NextButton
} from '../elements/';


class ImagesForm extends Component {

    render = () => {
        return(
            <React.Fragment>
                <div className="top-input-flex-container">
                    <ImageDropZone
                        id="UPLOAD_IMAGES"
                        onDragOver={ this.fileDropHover }
                        onDrop={ (e) => { this.props.uploadArtworkImages(e) } }
                    />
                </div>
                <NextButton onClick={ this.props.createArtwork }>Save</NextButton>
            </React.Fragment>
        )
    }


    fileDropHover = (e) => {
        e.preventDefault();
    }
}


export default ImagesForm;