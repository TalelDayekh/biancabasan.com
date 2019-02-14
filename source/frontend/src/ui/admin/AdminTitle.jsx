import React, { Component } from 'react';
// React Router
import { Redirect } from 'react-router-dom';
// Local imports
import TitleForm from './TitleForm.jsx';
import {
    AdminContentWrapper
} from '../layouts/';


class AdminTitle extends Component {

    componentDidMount = () => {
        this.props.resetRedirect()
    }
    render = () => {
        if (this.props.redirect.toAdminDetails === true) {
            return <Redirect push to="/admin/admin_details/"/>
        }
        if (this.props.redirect.toAdminMain === true) {
            return <Redirect push to="/admin/"/>
        }

        return(
            <AdminContentWrapper>
                <TitleForm
                    { ...this.props }
                    switchView={ this.switchView }
                />
            </AdminContentWrapper>
        )
    }


    switchView = (e) => {
        if (e.target.id === 'next') {
            this.props.toggleRedirect('ADMIN_DETAILS')
        };
        if (e.target.id === 'back') {
            this.props.toggleRedirect('ADMIN_MAIN')
        };
    }
}


export default AdminTitle;