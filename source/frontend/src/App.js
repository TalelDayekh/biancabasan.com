import React, { Component } from 'react';
// Redux
import { connect } from 'react-redux';
// React Router
import {
    BrowserRouter,
    Switch,
    Route
} from 'react-router-dom';
// Local imports
// Actions
import {
    loadArtworks
} from './actions/';
// Views
import Home from './ui/views/Home.jsx';
// Admin
import PrivateRoute from './ui/elements/PrivateRoute.jsx';
import AdminLogin from './ui/admin/AdminLogin.jsx';
import Admin from './ui/admin/Admin.jsx';


class App extends Component {

    componentDidMount = () => {
        // Get artworks from database
        this.props.loadArtworks();
    }

    render = () => {
        return(
            <BrowserRouter>
                <Switch>
                    {/* Views routes */}
                    <Route exact path='/' render={ () => (<Home { ...this.props }/>) }/>
                    {/* Admin routes */}
                    <Route path='/login/' render={ () => (<AdminLogin { ...this.props }/>) }/>
                    <PrivateRoute path='/admin/' render={ () => (<Admin { ...this.props }/>) }/>
                </Switch>
            </BrowserRouter>
        )
    }

}


// Entire app state
const mapStateToProps = (state) => {
    return {
        // Artwork related state
        retrieveArtwork: state.Artwork
    }
}

// All dispatch methods
const mapDispatchToProps = (dispatch) => {
    return {
        // GET requests
        loadArtworks: () => { dispatch(loadArtworks()) },
    }
}


export default connect(mapStateToProps, mapDispatchToProps)(App);