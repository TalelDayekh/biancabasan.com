import React, { Component } from 'react';
// Redux
import { connect } from 'react-redux';
// React Router
import { Redirect } from 'react-router-dom';
// Local imports
import {
    toggleRedirect,
    resetRedirect
} from '../../actions/';
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
            return <Redirect to="/admin/"/>
        }
        if (this.props.redirect.toAdminDetails === true) {
            return <Redirect to="/admin/admin_details/"/>
        }

        return(
            <AdminContentWrapper>
                <ImagesForm
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


export default connect(mapStateToProps, mapDispatchToProps)(AdminImages);