import React, { Component } from 'react'
// React Router
import { Redirect } from 'react-router-dom'
// Local imports
// Admin
import ImagesForm from './ImagesForm.jsx'


class AdminImages extends Component {

    render = () => {
        return(
            <React.Fragment>
                <ImagesForm
                    { ...this.props }
                />
            </React.Fragment>
        )
    }

}


export default AdminImages