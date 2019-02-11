// Local imports
import {
    loginAPI
} from '../actions/';


export function userLogin(username, password) {
    return (dispatch) => {
        dispatch(authStart());
        dispatch(loginAPI(username, password))
    }
}

export function authStart() {
    return {
        type: 'AUTH_START'
    }
}

export function authSuccess() {
    return {
        type: 'AUTH_SUCCESS'
    }
}

export function authFail(error) {
    return {
        type: 'AUTH_FAIL',
        payload: error
    }
}