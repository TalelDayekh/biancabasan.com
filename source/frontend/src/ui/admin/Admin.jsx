import React, { Component } from 'react';
// Redux
import { connect } from 'react-redux';
// React Router
import {
    Route
} from 'react-router-dom';
// Local imports
import {
    toggleRedirect,
    resetRedirect,
    setArtwork,
    createArtwork
} from '../../actions/'
import AdminTitle from './AdminTitle.jsx';
import AdminDetails from './AdminDetails.jsx';
import AdminImages from './AdminImages.jsx';
import {
    MainWrapper
} from '../layouts/';


class Admin extends Component {

    render = () => {
        return(
            <MainWrapper>
                <h1>ADMIN</h1>
                <Route path="/admin/admin_title/" render={ () => (<AdminTitle { ...this.props }/>) }/>
                <Route path="/admin/admin_details/" render={ () => (<AdminDetails { ...this.props }/>) }/>
                <Route path="/admin/admin_images" render={ () => (<AdminImages { ...this.props }/>) }/>
            </MainWrapper>
        )
    }
}


const mapStateToProps = (state) => {
    return {
        redirect: state.Redirect,
        retrieveArtwork: state.Artwork
    }
}
const mapDispatchToProps = (dispatch) => {
    return {
        resetRedirect: () => { dispatch(resetRedirect()) },
        toggleRedirect: (redirect_id) => {
            dispatch(toggleRedirect(redirect_id))
        },
        setArtwork: (e) => { 
            dispatch(setArtwork(e.target.id, e.target.value))
        },
        uploadArtworkImages: (e) => {
            dispatch(setArtwork(e.target.id, e.dataTransfer.files));
            e.preventDefault()
        },
        createArtwork: () => { dispatch(createArtwork()) }
    }
}


export default connect(mapStateToProps, mapDispatchToProps)(Admin);