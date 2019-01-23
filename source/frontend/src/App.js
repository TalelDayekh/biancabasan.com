import React, { Component } from 'react';
// Redux
import { Provider } from 'react-redux';
import store from './store.jsx';
// React Router
import {
    BrowserRouter,
    Route
} from 'react-router-dom';
// Local imports
import Admin from './ui/admin/Admin.jsx';


class App extends Component {

    render = () => {
        return(
            <Provider store = { store }>
                <BrowserRouter>
                    <Route path = "/admin/" component = { Admin } />
                </BrowserRouter>
            </Provider>
        )
    }
}


export default App;