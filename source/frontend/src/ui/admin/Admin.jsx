import React, { Component } from 'react'
// Redux
import { connect } from 'react-redux'
// React Router
import {
    Route
} from 'react-router-dom'
// Local imports
// Actions
import {
    toggleRedirect,
    toggleEditMode,
    resetRedirect,
    loadSortedArtworks,
    setInputErrors,
    setFormError,
    prepareImageUpload,
    setArtwork,
    deleteArtworksAPI
} from '../../actions/'
// Layouts
import {
    ModalWrapper
} from '../layouts/'
// Admin
import AdminMain from './AdminMain.jsx'
import AdminTitle from './AdminTitle.jsx'
import AdminDetails from './AdminDetails.jsx'
import AdminImages from './AdminImages.jsx'


class Admin extends Component {

    render = () => {
        return(
            <ModalWrapper>
                <h1>Admin</h1>
                { this.props.artworks.artworksLoading ?
                    <h2>Spinner...</h2>
                :
                    <React.Fragment>
                        <Route path='/admin/main' render={ () => (<AdminMain { ...this.props }/>) }/>
                        <Route path='/admin/title/' render={ () => (<AdminTitle { ...this.props }/>) }/>
                        <Route path='/admin/details/' render={ () => (<AdminDetails { ...this.props }/>) }/>
                        <Route path='/admin/images/' render={ () => (<AdminImages { ...this.props }/>) }/>
                    </React.Fragment>
                }
            </ModalWrapper>
        )
    }

}


const mapStateToProps = (state) => {
    return {
        admin: state.ArtworksAdmin,
        redirect: state.AdminRedirect
    }
}

const mapDispatchToProps = (dispatch) => {
    return {
        // Redirect
        toggleRedirect: (toAdminPanel) => { dispatch(toggleRedirect(toAdminPanel)) },
        toggleEditMode: (editMode, artworkId) => { dispatch(toggleEditMode(editMode, artworkId)) },
        resetRedirect: () => { dispatch(resetRedirect()) },
        // Artwork retrieve data
        loadSortedArtworks: () => { dispatch(loadSortedArtworks()) },
        // Artwork input data
        setInputErrors: (inputError, errorField) => { dispatch(setInputErrors(inputError, errorField)) },
        setFormError: (error) => { dispatch(setFormError(error)) },
        prepareImageUpload: (imageFile) => { dispatch(prepareImageUpload(imageFile)) },
        setArtwork: (inputFieldId, inputData) => { 
            dispatch(setArtwork(inputFieldId, inputData))
        },
        // DELETE requests
        deleteArtwork: (artworkId) => { dispatch(deleteArtworksAPI(artworkId)) }
    }
}


export default connect(mapStateToProps, mapDispatchToProps)(Admin)