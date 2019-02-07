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

    render = () => {
        return(
            <React.Fragment>
                <form id="next" onSubmit={ this.redirect }>
                    <div className = "top-input-flex-container">
                        <LongInputField
                            id="SET_TITLE"
                            size="1"
                            placeholder={ this.title }
                            // onFocus = ""
                            onBlur={ this.inputValidation }
                            defaultValue={ this.props.retrieveArtwork.title }
                            onChange={ (e) => { this.props.setArtwork(e) } }
                            raiseError={ this.props.retrieveArtwork.formValidationError ? true : undefined }
                        />
                    </div>
                    <NextButton type="submit">Next</NextButton>
                </form>
                <BackButton id="back" onClick={ this.redirect }>Back</BackButton>
            </React.Fragment>
        )
    }


    redirect = (e) => {
        this.props.redirect(e);
        e.preventDefault();
    }

    // Form validation
    inputValidation = () => {
        let RegEx = /^\d{4}$/
        if (!(this.props.retrieveArtwork.title.match(RegEx))) {
            this.props.inputError(true)
        }
    }
}


export default TitleForm;