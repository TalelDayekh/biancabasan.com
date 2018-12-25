import React, { Component } from 'react';
import axios from 'axios';
import { Redirect } from 'react-router-dom';
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
        artworkObjectId: "",
        // Input error
        incorrectInput: false,
        // Redirect
        toAddDetails: false
    }

    // Variable for input field placeholder
    title = "Title*"


    render = () => {
        // Redirect to AddDetails component and pass
        // id for the newly created artwork object
        if (this.state.toAddDetails === true) {
            return <Redirect to = {{
                pathname: "/admin/add_details/",
                state: { artworkObjectId: this.state.artworkObjectId }
            }} />
        }


        return(
            <AdminContentWrapper>
                {/* Heading */}
                <AdminHeading>
                    Did you make a new piece? Cool! What's it called?
                </AdminHeading>

                <form onSubmit = { this.createTitle }>
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
                    <SaveButton type = "submit">Save</SaveButton>
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

    createTitle = (event) => {
        axios.post('http://localhost:8000/admin_artworks/add_title/', {
            owner: "1", // !! REMOVE HARD CODED OWNER !!
            title: this.state.title
        }).then(response => {
            this.setState({
                artworkObjectId: response.data.id,
                toAddDetails: true
            })
        });
        event.preventDefault();
    }

}


export default AddTitle;