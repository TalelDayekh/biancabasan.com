import React, { Component } from 'react';
import axios from 'axios';
import TitleForm from './TitleForm.jsx';
import {
    AdminContentWrapper,
    AdminHeading
} from '../elements/';


class AdminTitle extends Component {

    state = {
        // Retrieved data
        retrievedTitle: "",
        // Toggle edit mode
        editTitleMode: false
    }


    componentDidMount = () => {
        axios.get('http://localhost:8000/admin_artworks/artworks_list/').then(res => {
            // If artwork object exists go ahead
            // and save artwork title to state
            let retrievedArtworkObject = null
            if (retrievedArtworkObject = res.data.find((artworkObject) => artworkObject.id === 38)) {
                this.setState({
                    retrievedTitle: retrievedArtworkObject.title,
                    editTitleMode: true
                })
            }
        })
    }

    render = () => {
        return(
            <AdminContentWrapper>
                {/* Heading */}
                <AdminHeading>
                    Did you make a new piece? Cool! What's it called?
                </AdminHeading>

                {/* Title form */}
                <TitleForm 
                />
            </AdminContentWrapper>
        )
    }
}


export default AdminTitle;