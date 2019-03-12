import React, { Component } from 'react'
// React Router
import { Redirect } from 'react-router-dom'
// Local imports
// Admin
import DetailsForm from './DetailsForm.jsx'


class AdminDetails extends Component {

    render = () => {
        if (this.props.redirect.toAdminImages) {
            return <Redirect push to='/admin/images/'/>
        }
        if (this.props.redirect.toAdminTitle) {
            return <Redirect push to='/admin/title/'/>
        }

        return(
            <React.Fragment>
                <DetailsForm
                    { ...this.props }
                    switchAdminPanel={ this.switchAdminPanel }
                />
            </React.Fragment>
        )
    }


    // Trigger state change to redirect the user
    // either to next or previous admin panel.
    switchAdminPanel = (e) => {
        if (e.target.id==='next') {
            this.props.toggleRedirect('ADMIN_IMAGES')
        }
        if (e.target.id==='back') {
            this.props.toggleRedirect('ADMIN_TITLE')
        }
    }

}


export default AdminDetails