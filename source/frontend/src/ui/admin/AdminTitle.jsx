import React, { Component } from 'react';
import axios from 'axios';
import { Redirect } from 'react-router-dom';
import TitleForm from './TitleForm.jsx';
import {
    AdminContentWrapper,
    AdminHeading
} from '../elements/';


class AdminTitle extends Component {

    state = {
        artworkObjectId: "",
        // Retrieved data
        retrievedTitle: "",
        // Toggle edit mode
        editTitleMode: false,
        // Redirect
        toAddDetails: false
    }


    componentDidMount = () => {
        axios.get('http://localhost:8000/admin_artworks/artworks_list/').then(res => {
            // If artwork object exists go ahead
            // and save artwork title to state
            let retrievedArtworkObject = null
            if (retrievedArtworkObject = res.data.find((artworkObject) => artworkObject.id === 338)) {
                this.setState({
                    retrievedTitle: retrievedArtworkObject.title,
                    editTitleMode: true
                })
            }
        })
    }

    render = () => {
        // Redirect to AdminDetails component
        // and pass id for the artwork object
        if (this.state.toAddDetails === true) {
            return <Redirect to = {{
                pathname: "/admin/add_details/", // !! CHANGE PATH NAME !!
                state: { artworkObjectId: this.state.artworkObjectId } 
            }} />
        }

        return(
            <AdminContentWrapper>
                {/* Heading */}
                <AdminHeading>
                    Did you make a new piece? Cool! What's it called?
                </AdminHeading>

                {/* Title form */}
                <TitleForm
                    editMode = { this.state.editTitleMode }
                    retrievedTitle = { this.state.retrievedTitle }
                    createTitle = { this.createTitle }
                    editTitle = { this.editTitle }
                />
            </AdminContentWrapper>
        )
    }


    createTitle = (inputData) => {
        axios.post('http://localhost:8000/admin_artworks/add_title/', {
            owner: "1", // !! REMOVE HARD CODED OWNER !!
            title: inputData
        }).then(res => {
            this.setState({
                artworkObjectId: res.data.id,
                toAddDetails: true
            })
        })
    }

    editTitle = (inputData) => {
        // let id = 38
        // axios.put('http://localhost:8000/admin_artworks/edit_title/'+id, {
        //     owner: "1", // !! REMOVE HARD CODED OWNER !!
        //     title: inputData
        // }).then(response => {console.log(response.data)})
    }
}


export default AdminTitle;