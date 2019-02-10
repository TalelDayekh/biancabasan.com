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
import PrivateRoute from './ui/elements/PrivateRoute.jsx';
import AdminLogin from './ui/admin/AdminLogin.jsx';
import Admin from './ui/admin/Admin.jsx';


class App extends Component {

    render = () => {
        return(
            <Provider store = { store }>
                <BrowserRouter>
                    <React.Fragment>
                        <Route path="/login/" component={ AdminLogin }/>
                        <PrivateRoute path="/admin/" component={ Admin }/>
                    </React.Fragment>
                </BrowserRouter>
            </Provider>
        )
    }
}


export default App;