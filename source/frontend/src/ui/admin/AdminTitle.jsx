import React, { Component } from 'react'
// React Router
import { Redirect } from 'react-router-dom'
// Local imports
// Admin
import TitleForm from './TitleForm.jsx'


class AdminTitle extends Component {

    render = () => {
        if (this.props.redirect.toAdminMain) {
            return <Redirect push to='/admin/main/'/>
        }
        if (this.props.redirect.toAdminDetails) {
            return <Redirect push to='/admin/details/'/>
        }

        return(
            <React.Fragment>
                <TitleForm
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
            this.props.toggleRedirect('ADMIN_DETAILS')
        }
        if (e.target.id==='back') {
            this.props.toggleRedirect('ADMIN_MAIN')
        }
    }

}


export default AdminTitle