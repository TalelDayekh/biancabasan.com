import React, { Component } from 'react';

import { BrowserRouter, Route } from 'react-router-dom';

import AddTitle from './admin_views/AddTitle';
import AddDetails from './admin_views/AddDetails';


class App extends Component {
    render() {
        return (
            <BrowserRouter>
                <div>
                    <Route path="/admin_add_title" component={ AddTitle } />
                    <Route path="/admin_add_details" component={ AddDetails } />
                </div>
            </BrowserRouter>
        )
    }
}


export default App;