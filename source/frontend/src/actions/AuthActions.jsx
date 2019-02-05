// Axios
import axios from 'axios';


export function userLogin(username, password) {
    return (dispatch) => {
        dispatch(authStart());
        axios.post('http://localhost:8000/auth/login/', {
            username: username,
            password: password
        }).then(res => {
            const token = res.data.key;
            sessionStorage.setItem('token', token);
            console.log(token); // !! REMOVE CONSOLE LOG
            dispatch(authSuccess(token));
        })
    }
}

export function userLogout() {
    return {
        type: ''
    }
}

export function authStart() {
    return {
        type: 'AUTH_START'
    }
}

export function authSuccess(token) {
    return {
        type: 'AUTH_SUCCESS',
        payload: token
    }
}

export function authFail(error) {
    return {
        type: 'AUTH_FAIL',
        payload: error
    }
}