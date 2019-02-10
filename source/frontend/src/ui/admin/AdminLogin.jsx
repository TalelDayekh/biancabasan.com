import React, { Component } from 'react';
// Redux
import { connect } from 'react-redux';
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
        return(
            <React.Fragment>
                <h2>LOGIN</h2>
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
            </React.Fragment>
        )
    }
}


const mapDispatchToProps = (dispatch) => {
    return {
        loginUser: (e, username, password) => { dispatch(userLogin(username, password)); e.preventDefault() }
    }
}


export default connect(null, mapDispatchToProps)(AdminLogin);