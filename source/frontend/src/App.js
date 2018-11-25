import React, { Component } from 'react';

import { BrowserRouter, Route } from 'react-router-dom';

import AddTitle from './admin_views/AddTitle';
import AddDetails from './admin_views/AddDetails';
import AddImages from './admin_views/AddImages';


class App extends Component {
    render() {
        return (
            <BrowserRouter>
                <div>
                    <Route path="/admin_add_title/" component={ AddTitle } />
                    <Route path="/admin_add_details/" component={ AddDetails } />
                    <Route path="/admin_add_images/" component={ AddImages } />
                </div>
            </BrowserRouter>
        )
    }
}


export default App;