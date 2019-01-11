import React, { Component } from 'react';
import axios from 'axios';
import DetailsForm from './DetailsForm.jsx';
import {
    AdminContentWrapper,
    AdminHeading
} from '../elements/';


class AdminDetails extends Component {

    state = {
        // Retrieved data
        retrievedDetails: {},
        // Toggle edit mode
        editDetailsMode: false
    }


    componentDidMount = () => {
        axios.get('http://localhost:8000/admin_artworks/artworks_list/').then(res => {
            // If artwork object exist and details
            // for that very same object exist go
            // ahead and save details to state
            let retrievedArtworkObject = null
            let retrievedArtworkObjectDetails = null
            let detailsObject = null

            if (retrievedArtworkObject = res.data.find((artworkObject) => artworkObject.id === 38)) {
                retrievedArtworkObjectDetails = retrievedArtworkObject.details

                if (retrievedArtworkObjectDetails.title === 38) {
                    detailsObject = Object.assign({}, retrievedArtworkObjectDetails);
                    delete detailsObject.id;
                    delete detailsObject.title;
                    this.setState({
                        retrievedDetails: detailsObject,
                        editDetailsMode: true
                    })
                }
            }
        })
    }

    render = () => {
        return(
            <AdminContentWrapper>
                {/* Heading */}
                <AdminHeading>
                    Add some specs and describe your work a bit
                </AdminHeading>

                {/* Details form */}
                <DetailsForm
                    retrievedDetails = { this.state.retrievedDetails }
                />
            </AdminContentWrapper>
        )
    }
}


export default AdminDetails;