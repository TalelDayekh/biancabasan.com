import React, { Component } from 'react';
// Local imports
import ImagesForm from './ImagesForm.jsx';
import {
    AdminContentWrapper
} from '../layouts/';


class AdminImages extends Component {

    render = () => {
        return(
            <AdminContentWrapper>
                <ImagesForm
                />
            </AdminContentWrapper>
        )
    }
}


export default AdminImages;