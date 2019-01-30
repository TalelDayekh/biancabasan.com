import React, { Component } from 'react';
// Redux
import { connect } from 'react-redux';
// React Router
import { Redirect } from 'react-router-dom';
// Local imports
import {
    toggleRedirect,
    resetRedirect
} from '../../actions/'
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
            return <Redirect to="/admin/admin_images/"/>
        }
        if (this.props.redirect.toAdminTitle === true) {
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
        if (e.target.id === 'next') {
            this.props.toggleRedirect('ADMIN_IMAGES')
        };
        if (e.target.id === 'back') {
            this.props.toggleRedirect('ADMIN_TITLE')
        }
    }
}


const mapStateToProps = (state) => {
    return {
        redirect: state.Redirect
    }
}

const mapDispatchToProps = (dispatch) => {
    return {
        resetRedirect: () => { dispatch(resetRedirect()) },
        toggleRedirect: (redirect_id) => {
            dispatch(toggleRedirect(redirect_id))
        }
    }
}


export default connect(mapStateToProps, mapDispatchToProps)(AdminDetails);