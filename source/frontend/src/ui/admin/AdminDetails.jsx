import React, { Component } from 'react';
// React Router
import { Redirect } from 'react-router-dom';
// Local imports
import DetailsForm from './DetailsForm.jsx';
import {
    AdminContentWrapper
} from '../layouts/';


class AdminDetails extends Component {

    componentDidMount = () => {
        this.props.resetRedirect();
    }
    render = () => {
        if (this.props.redirect.toAdminImages === true) {
            return <Redirect push to="/admin/admin_images/"/>
        }
        if (this.props.redirect.toAdminTitle === true) {
            return <Redirect push to="/admin/admin_title/"/>
        }

        return(
            <AdminContentWrapper>
                <DetailsForm
                    { ...this.props }
                    switchView={ this.switchView }
                />
            </AdminContentWrapper>
        )
    }


    switchView = (e) => {
        if (e.target.id === 'next') {
            this.props.toggleRedirect('ADMIN_IMAGES')
        };
        if (e.target.id === 'back') {
            this.props.toggleRedirect('ADMIN_TITLE')
        }
    }
}


export default AdminDetails;