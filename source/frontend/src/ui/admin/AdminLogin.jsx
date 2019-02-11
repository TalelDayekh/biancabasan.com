import React, { Component } from 'react';
// Redux
import { connect } from 'react-redux';
// React Router
import {
    Redirect
} from 'react-router-dom';
// Local imports
import {
    userLogin
} from '../../actions/';


class AdminLogin extends Component {

    constructor(props) {
        super(props);
        this.unameInput = React.createRef();
        this.pswInput = React.createRef();
    }


    render = () => {
        if (this.props.auth.token !== null) {
            return <Redirect push to="/admin/"/>
        }

        return(
            <React.Fragment>
                {
                    this.props.auth.isLoading ?
                    <h2>Loading...</h2> // !! CHANGE TO SPINNER
                    :
                    <form onSubmit={(e) => { 
                        this.props.loginUser(
                            e,
                            this.unameInput.current.value,
                            this.pswInput.current.value
                            ) 
                        }}>
                        <label>Username</label>
                        <br/>
                        <input ref={ this.unameInput } type="text"/>
                        <br/>
                        <br/>
                        <label>Password</label>
                        <br/>
                        <input ref={ this.pswInput } type="password"/>
                        <br/>
                        <button type="submit">Login</button>
                    </form>
                }
            </React.Fragment>
        )
    }
}


const mapStateToProps = (state) => {
    return {
        auth: state.Auth
    }
}


const mapDispatchToProps = (dispatch) => {
    return {
        loginUser: (e, username, password) => { dispatch(userLogin(username, password)); e.preventDefault() }
    }
}


export default connect(mapStateToProps, mapDispatchToProps)(AdminLogin);