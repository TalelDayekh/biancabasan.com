import React, { Component } from 'react';
// Redux
import { connect } from 'react-redux';
// Local imports
import '../../App.css';
import {
    setArtwork,
    createArtwork
} from '../../actions/';
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
                        onDrop={ (e) => { this.props.setArtwork(e)} }
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


const mapStateToProps = (state) => {
    return {
        retrieveArtwork: state.Artwork
    }
}


const mapDispatchToProps = (dispatch) => {
    return {
        setArtwork: (e) => {
            dispatch(setArtwork(e.target.id, e.dataTransfer.files));
            e.preventDefault()
        },
        createArtwork: () => { dispatch(createArtwork()) }
    }
}


export default connect(mapStateToProps, mapDispatchToProps)(ImagesForm);