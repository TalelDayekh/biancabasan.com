import React, { Component } from 'react';
import './Admin.css';
import {
    LongInputField,
    SaveButton,
    BackButton
} from '../elements/';


class TitleForm extends Component {

    state = {
        title: "",
        // Edit mode
        editTitleMode: false,
        // Input error
        incorrectInput: false
    }

    // Variable for input field placeholder
    title = "Title*"


    // Change state based on props
    // to prepare form for edit mode
    static getDerivedStateFromProps = (props, state) => {
        if (props.editMode != state.editTitleMode) {
            return {
                editTitleMode: props.editMode,
                title: props.retrievedTitle
            };
        }
        return null;
    }

    render = () => {
        return(
            <form onSubmit = { this.dbRequest }>
                {/* Input field */}
                {/* Title */}
                <div className= "top-input-flex-container">
                    <LongInputField
                        id = "title"
                        size = "1"
                        placeholder = { this.title }
                        onFocus = { this.clearPlaceholder }
                        onBlur = { this.inputValidation }
                        defaultValue = { this.state.editTitleMode ? 
                            this.props.retrievedTitle : 
                            this.state.title }
                        onChange = { this.updateTitleState }
                        raiseError = { this.state.incorrectInput ? true : undefined }
                    />
                </div>

                {/* Buttons */}
                <SaveButton type="submit">Save</SaveButton>
                <BackButton>Back</BackButton>
            </form>
        )
    }


    updateTitleState = (e) => {
        this.setState({
            [e.target.id]: e.target.value
        })
    }

    clearPlaceholder = (e) => {
        e.target.placeholder = ""
    }

    inputValidation = (e) => {
        if (this.state.title.length === 0) {
            this.setState({
                incorrectInput: true
            });
            e.target.placeholder = "PLACEHOLDER TEXT"
        }
    }

    dbRequest = (e, inputData) => {
        inputData = this.state.title;

        if (this.state.incorrectInput === false) {
            if (this.state.editTitleMode === false) {
                this.props.createTitle(inputData)
            }
            if (this.state.editTitleMode === true) {
                this.props.editTitle(inputData)
            }
        };
        e.preventDefault();
    }
}


export default TitleForm;