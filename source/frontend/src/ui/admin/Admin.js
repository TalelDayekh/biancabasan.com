import React, { Component } from 'react';

import styled, { createGlobalStyle } from 'styled-components';

import {
    BrowserRouter,
    Route,
    Link
} from 'react-router-dom';

import { MainWrapper } from '../elements/Wrappers';

import AddTitle from './AddTitle';



const AdminOverlay = createGlobalStyle`
    body {
        background: rgba(58, 66, 90, 0.7);
        backdrop-filter: blur(25px);
    }
`


class Admin extends Component {

    render = () => {
        return(
            <BrowserRouter>
                    <MainWrapper>
                    <AdminOverlay />
                        <p>Hello World</p>
                        <Route path='/admin/add_title/' component={ AddTitle } />
                    </MainWrapper>
            </BrowserRouter>
        )
    }

}


export default Admin;