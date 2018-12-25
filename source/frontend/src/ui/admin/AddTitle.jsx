import React, { Component } from 'react';
import axios from 'axios';
import './Admin.css';
import {
    AdminContentWrapper,
    AdminHeading,
    LongInputField,
    SaveButton,
    BackButton
} from '../elements/';


class AddTitle extends Component {

    state = {
        title: "",
        // Input error
        incorrectInput: false
    }

    // Variable for input field placeholder
    title = "Title*"


    render = () => {
        return(
            <AdminContentWrapper>
                {/* Heading */}
                <AdminHeading>
                    Did you make a new piece? Cool! What's it called?
                </AdminHeading>

                <form>
                    {/* Input field */}
                    {/* Title */}
                    <div className = "top-input-flex-container">
                        <LongInputField
                            id = "title"
                            size = "1"
                            placeholder = { this.title }
                            onFocus = { this.clearPlaceholder }
                            onBlur = { this.inputValidation }
                            value = { this.state.title }
                            onChange = { this.updateTitleState }
                            raiseError = { this.state.incorrectInput ? true : undefined }
                        />
                    </div>

                    {/* Buttons */}
                    <SaveButton>Save</SaveButton>
                    <BackButton>Back</BackButton>
                </form>
            </AdminContentWrapper>
        )
    }


    updateTitleState = (event) => {
        this.setState({
            [event.target.id]: event.target.value,
            incorrectInput: false
        })
    }

    clearPlaceholder = (event) => {
        event.target.placeholder = ""
    }

    inputValidation = (event) => {
        if (this.state.title.length === 0) {
            this.setState({
                incorrectInput: true
            });
            event.target.placeholder = "PLACEHOLDER TEXT"
        }
    }

    createTitle = () => {

    }

}


export default AddTitle;