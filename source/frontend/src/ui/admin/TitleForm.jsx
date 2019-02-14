import React, { Component } from 'react';
// Local imports
import '../../App.css';
import {
    LongInputField,
    NextButton,
    BackButton
} from '../elements/';


class TitleForm extends Component {

    // Variable for input field placeholder
    title="Title*"

    componentDidMount = () => {
        if (this.props.redirect.editMode === true) {
            Object.values(this.props.retrieveArtworks.artworksList).forEach((artworkObject) => {
                let artworkToEdit = artworkObject.find(
                    getArtwork => getArtwork.id === this.props.retrieveArtworks.artworkObjectId
                    );
                if (artworkToEdit) {
                    this.props.editArtwork(artworkToEdit)
                };
            });
        };
    }
    render = () => {
        return(
            <React.Fragment>
                <form id="next" onSubmit={ this.switchView }>
                    <div className = "top-input-flex-container">
                        <LongInputField
                            id="SET_TITLE"
                            size="1"
                            placeholder={ this.title }
                            // onFocus = ""
                            onBlur={ this.inputValidation }
                            defaultValue={ this.props.redirect.editMode ?
                                this.props.retrieveArtworks.editArtwork.title
                                :
                                this.props.retrieveArtworks.title }
                            onChange={ (e) => { this.props.setArtwork(e) } }
                            raiseError={ this.props.retrieveArtworks.formValidationError ? true : undefined }
                        />
                    </div>
                    <NextButton type="submit">Next</NextButton>
                </form>
                <BackButton id="back" onClick={ this.switchView }>Back</BackButton>
            </React.Fragment>
        )
    }


    switchView = (e) => {
        this.props.switchView(e);
        e.preventDefault();
    }

    // Form validation
    inputValidation = () => {
        let RegEx = /^\d{4}$/
        if (!(this.props.retrieveArtworks.title.match(RegEx))) {
            this.props.inputError(true)
        }
    }
}


export default TitleForm;