import React, { Component } from 'react';

import axios from 'axios';

import {
    Link,
    Redirect
} from 'react-router-dom';

import { AdminContentWrapper } from '../layouts/Wrappers';
import { AdminHeading } from '../elements/Headings'
import { LongInputField } from '../elements/InputFields';
import { SaveButton, BackButton } from '../elements/Buttons';


const headingStyle = {
    marginTop: '160px'
}

const inputContainer = {
    display: 'flex',
    marginTop: '55px'
}

const saveButtonStyle = {
    float: 'left',
    marginTop: '22px'
}

const backButtonStyle = {
    float: 'left',
    margin: '22px 0px 0px 10px'
}


class AddTitle extends Component {

    state = {
        toAddDetails: false,
        title: "",
        artworkObjectId: ""
    }


    // Variable for input field placeholder
    title = "Title*"


    render = () => {

        // Redirect to AddDetails component and pass state
        // with id for the newly created artwork object
        if (this.state.toAddDetails === true) {
            return <Redirect to = {{
                pathname: "/admin/add_details",
                state: { artworkObjectId: this.state.artworkObjectId }
            }} />
        }


        return(
            <AdminContentWrapper>
                {/* Heading */}
                <AdminHeading style = { headingStyle }>
                    Did you make a new piece? Cool! What's it called?
                </AdminHeading>

                <form onSubmit = { this.createTitle }>
                    {/* Input field */}
                    {/* Title */}
                    <div style = { inputContainer }>
                        <LongInputField
                            size = "1"
                            placeholder = { this.title }
                            onFocus = { this.clearPlaceholder }
                            onBlur = { (event) => event.target.placeholder = this.title }
                            value = { this.state.title }
                            onChange = { this.updateTitleState }
                        />
                    </div>

                    {/* Buttons */}
                    <SaveButton style = { saveButtonStyle } type = "submit">Save</SaveButton>
                    <Link to = "/admin/">
                        <BackButton style = { backButtonStyle }>Back</BackButton>
                    </Link>
                </form>
            </AdminContentWrapper>
        )
    }


    clearPlaceholder = (event) => {
        event.target.placeholder = ""
    }

    updateTitleState = (event) => {
        this.setState({
            title: event.target.value
        })
    }

    createTitle = (event) => {
        // !! REMOVE HARDCODED OWNER FROM POST REQUEST !!
        axios.post('http://localhost:8000/admin_artworks/add_title/', { owner: "1", title: this.state.title })
        .then(response => {
            this.setState({
                artworkObjectId: response.data.id,
                toAddDetails: true
            })
        });
        event.preventDefault();
    }

}


export default AddTitle;