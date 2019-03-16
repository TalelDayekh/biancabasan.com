// Local imports
import {
    userLoginAPI
} from '../actions/'


export function loginUser(username, password) {
    return (dispatch) => {
        dispatch(userLoginAPI(username, password))
    }
}

export function authenticationSuccess() {
    return {
        type: 'AUTH_SUCCESS'
    }
}

export function loginFailError(error) {
    return {
        type: 'AUTH_FAIL',
        payload: error
    }
}