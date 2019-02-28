const defaultState = {
    token: null,
    userLoaded: false,
    loadingError: false
}


const Authentication = (state = defaultState, action) => {
    switch(action.type) {

        case 'AUTH_SUCCESS':
            return state = {
                ...state,
                token: sessionStorage.getItem('token'),
                userLoaded: true,
                loadingError: false
            }
        case 'AUTH_FAIL':
            return state = {
                ...state,
                userLoaded: false,
                loadingError: action.payload
            }

        default:
            return state
    }
}


export default Authentication