// Axios
import axios from 'axios'
// Local imports
import {
    userLoginAPI
} from '../actions/'


export function loginUser(username, password) {
    return (dispatch) => {
        dispatch(userLoginAPI(username, password))
    }
}

// Set authentication token globally in
// headers for all axios requests.
export function authenticationSuccess() {
    return (dispatch) => {
        axios.defaults.headers.common = {'Authorization': `token ${sessionStorage.getItem('token')}`}
        dispatch({
            type: 'AUTH_SUCCESS'
        })
    }
}

export function loginFailError(error) {
    return {
        type: 'AUTH_FAIL',
        payload: error
    }
}