import React, { Component } from 'react';
// React Router
import { Redirect } from 'react-router-dom';
// Local imports
import ImagesForm from './ImagesForm.jsx';
import {
    AdminContentWrapper
} from '../layouts/';


class AdminImages extends Component {

    componentDidMount = () => {
        this.props.resetRedirect();
    }
    render = () => {
        if (this.props.redirect.toAdminMain === true) {
            return <Redirect push to="/admin/"/>
        }
        if (this.props.redirect.toAdminDetails === true) {
            return <Redirect push to="/admin/admin_details/"/>
        }

        return(
            <AdminContentWrapper>
                <ImagesForm
                    { ...this.props }
                />
            </AdminContentWrapper>
        )
    }


    redirect = (e) => {
        if (e.target.id === 'next') {
            this.props.toggleRedirect('ADMIN_MAIN')
        };
        if (e.target.id === 'back') {
            this.props.toggleRedirect('ADMIN_DETAILS')
        };
    }
}


export default AdminImages;