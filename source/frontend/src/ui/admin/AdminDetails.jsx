import React, { Component } from 'react';
// React Router
import { Redirect } from 'react-router-dom';
// Local imports
import DetailsForm from './DetailsForm.jsx';
import {
    AdminContentWrapper
} from '../layouts/';


class AdminDetails extends Component {

    state = {
        // Redirect
        toAdminTitle: false,
        toAdminImages: false
    }


    render = () => {
        if (this.state.toAdminImages === true) {
            return <Redirect to="/admin/admin_images/"/>
        }

        if (this.state.toAdminTitle === true) {
            return <Redirect to="/admin/admin_title/"/>
        }

        return(
            <AdminContentWrapper>
                <DetailsForm
                    redirect={ this.redirect }
                />
            </AdminContentWrapper>
        )
    }


    redirect = (e) => {
        if (e.target.id === "next") {
            this.setState({
                toAdminImages: true
            })
        };
        if (e.target.id === "back") {
            this.setState({
                toAdminTitle: true
            })
        }
    }
}


export default AdminDetails;