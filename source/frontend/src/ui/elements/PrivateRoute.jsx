import React from 'react';
// Redux
import { connect } from 'react-redux';
// React Router
import {
    Route,
    Redirect
} from 'react-router-dom';


const PrivateRoute = ({ component: Component, auth, ...rest}) => (
    <Route { ...rest } render={(props) => {
        if (auth.token !== null) {
            return <Component { ...props }/>
        } else {
            return <Redirect push to="/login/"/>
        }
    }}/>
)


const mapStateToProps = (state) => {
    return {
        auth: state.Auth
    }
}


export default connect(mapStateToProps)(PrivateRoute);