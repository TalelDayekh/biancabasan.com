import React, { Component } from 'react';
// React Router
import {
    Route
} from 'react-router-dom';
// Local imports
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
                <Route path = "/admin/admin_title/" component = { AdminTitle }/>
                <Route path = "/admin/admin_details"  component = { AdminDetails }/>
                <Route path = "/admin/admin_images/" component = { AdminImages }/>
            </MainWrapper>
        )
    }
}


export default Admin;