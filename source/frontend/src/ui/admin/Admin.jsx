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
    loadSortedArtworks
} from '../../actions/'
// Layouts
import {
    ModalWrapper
} from '../layouts/'
// Admin
import AdminMain from './AdminMain.jsx'


class Admin extends Component {

    render = () => {
        return(
            <ModalWrapper>
                <h1>Admin</h1>
                { this.props.artworks.artworksLoading ?
                    <h2>Spinner...</h2>
                :
                    <Route path='/admin/main' render={ () => (<AdminMain { ...this.props }/>) }/>
                }
            </ModalWrapper>
        )
    }

}


const mapStateToProps = (state) => {
    return {
        admin: state.ArtworksAdmin
    }
}

const mapDispatchToProps = (dispatch) => {
    return {
        // Artwork retrieve data
        loadSortedArtworks: () => { dispatch(loadSortedArtworks()) }
    }
}


export default connect(mapStateToProps, mapDispatchToProps)(Admin)