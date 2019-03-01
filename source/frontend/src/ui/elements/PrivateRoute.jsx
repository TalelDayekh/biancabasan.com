import React from 'react'
// React Router
import {
    Route,
    Redirect
} from 'react-router-dom'


const PrivateRoute = ({ component: Component, globalReduxProps, ...rest}) => (
    <Route { ...rest } render={ (props) => {
        if (globalReduxProps.auth.token !== null) {
            return <Component { ...props } { ...globalReduxProps }/>
        } else {
            return <Redirect push to='/login/'/>
        }
    }}/>
)


export default PrivateRoute