import React, { Component } from 'react';
// Redux
import { connect } from 'react-redux';
// React Router
import {
    Route
} from 'react-router-dom';
// Local imports
import {
    resetRedirect,
    toggleRedirect,
    toggleEditMode,
    setArtwork,
    editArtwork,
    inputError,
    loadArtworks,
    createArtwork
} from '../../actions/';
import AdminMain from './AdminMain.jsx';
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
                <Route path="/admin/main/" render={ () => (<AdminMain { ...this.props }/>) }/>
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
        retrieveArtworks: state.Artwork
    }
}
const mapDispatchToProps = (dispatch) => {
    return {
        // Redirect
        resetRedirect: () => { dispatch(resetRedirect()) },
        toggleRedirect: (redirect_id) => { dispatch(toggleRedirect(redirect_id)) },
        toggleEditMode: (activateEditMode, artworkId) => { dispatch(toggleEditMode(activateEditMode, artworkId)) },
        // Artwork input data
        setArtwork: (e) => {
            dispatch(setArtwork(e.target.id, e.target.value));
            dispatch(inputError(false));
        },
        uploadArtworkImages: (e) => {
            dispatch(setArtwork(e.target.id, e.dataTransfer.files));
            e.preventDefault();
        },
        editArtwork: (artworkToEdit) => { dispatch(editArtwork(artworkToEdit)) },
        inputError: (error) => { dispatch(inputError(error)) },
        // GET requests
        loadArtworks: () => { dispatch(loadArtworks()) },
        // POST requests
        createArtwork: () => { dispatch(createArtwork()) }
    }
}


export default connect(mapStateToProps, mapDispatchToProps)(Admin);