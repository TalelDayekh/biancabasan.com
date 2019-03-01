import React, { Component } from 'react'
// React Router
import {
    Redirect
} from 'react-router-dom'
// Local imports
// Layouts
import {
    ModalWrapper
} from '../layouts/'


class AdminLogin extends Component {

    constructor(props) {
        super(props)
        this.usernameInput = React.createRef()
        this.passwordInput = React.createRef()
    }

    render = () => {
        if (this.props.auth.token !== null) {
            return <Redirect push to='/admin/main/'/>
        }

        return(
            <ModalWrapper>
                { this.props.auth.userLoaded ?
                    <h2>Spinner...</h2>
                :
                    <form onSubmit={(e) => {
                        this.props.loginUser(this.usernameInput.current.value, this.passwordInput.current.value)
                        e.preventDefault()
                    }}>
                        <label>Username</label>
                        <br/>
                        <input ref={ this.usernameInput } type='text'/>
                        <br/>
                        <br/>
                        <label>Password</label>
                        <br/>
                        <input ref={ this.passwordInput } type='password'/>
                        <br/>
                        <br/>
                        <button type='submit'>Login</button>
                    </form>
                }
            </ModalWrapper>
        )
    }

}


export default AdminLogin