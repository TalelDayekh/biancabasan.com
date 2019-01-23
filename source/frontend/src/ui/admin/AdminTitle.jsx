import React, { Component } from 'react';
// React Router
import { Redirect } from 'react-router-dom';
// Local imports
import TitleForm from './TitleForm.jsx';
import {
    AdminContentWrapper
} from '../layouts/';


class AdminTitle extends Component {

    state = {
        // Redirect
        toAdminDetails: false
    }


    render = () => {
        if (this.state.toAdminDetails === true) {
            return <Redirect to="/admin/admin_details/"/>
        }

        return(
            <AdminContentWrapper>
                <TitleForm
                    redirect={ this.redirect }
                />
            </AdminContentWrapper>
        )
    }


    redirect = (e) => {
        if (e.target.id === "next") {
            this.setState({
                toAdminDetails: true
            })
        };
        if (e.target.id === "back") {
            this.setState({

            })
        }
    }
}


export default AdminTitle;