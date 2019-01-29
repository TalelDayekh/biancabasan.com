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
            return <Redirect to="/admin/admin_details/"/>
        }
        if (this.props.redirect.toAdminMain === true) {
            return <Redirect to="/admin/"/>
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
        if (e.target.id === 'next') {
            this.props.toggleRedirect('ADMIN_DETAILS')
        };
        if (e.target.id === 'back') {
            this.props.toggleRedirect('ADMIN_MAIN')
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


export default connect(mapStateToProps, mapDispatchToProps)(AdminTitle);