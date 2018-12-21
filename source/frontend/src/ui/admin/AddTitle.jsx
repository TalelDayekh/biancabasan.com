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
    marginTop: '230px',
}

const titleInputStyle = {
    marginTop: '55px',
}

const saveButtonStyle = {
    float: 'left',
    marginTop: '22px',
}

const backButtonStyle = {
    float: 'left',
    marginTop: '22px',
    marginLeft: '10px',
}


class AddTitle extends Component {

    state = {
        toAddDetails: false,
        title: "",
        artworkObjectId: "",
    }


    render = () => {

        // If true, redirect to AddDetails component
        // and pass the state with id for the newly
        // created artwork object
        if (this.state.toAddDetails === true) {
            return <Redirect to={{
                pathname: "/admin/add_details",
                state: { artworkObjectId: this.state.artworkObjectId }
            }} />
        }

        return(
            <AdminContentWrapper>
                {/* Heading */}
                <div>
                    <AdminHeading style={ headingStyle }>
                        Did you make a new piece? Cool! What's it called?
                    </AdminHeading>
                </div>

                <form onSubmit={ this.createTitle }>
                    {/* Input field */}
                    <LongInputField
                        name="Title"
                        placeholder="Title" 
                        style={ titleInputStyle }
                        onFocus={(event) => { event.target.placeholder = "" }}
                        onBlur={(event) => { event.target.placeholder = event.target.name }}
                        onChange={ this.updateTitleState }
                        value={ this.state.title }
                    />

                    {/* Buttons */}
                    <SaveButton style={ saveButtonStyle } type="submit">Save</SaveButton>
                    <Link to="/admin/">
                        <BackButton style={ backButtonStyle }>Back</BackButton>
                    </Link>
                </form>
            </AdminContentWrapper>
        )
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