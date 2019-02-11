const defaultState = {
    isLoading: false,
    token: sessionStorage.getItem('token'),
    error: false
}


const Auth = (state = defaultState, action) => {
    switch (action.type) {
        case 'AUTH_START':
            return state = {
                ...state,
                isLoading: true,
                error: false
            };
        case 'AUTH_SUCCESS':
            return state = {
                ...state,
                isLoading: false,
                token: sessionStorage.getItem('token'),
                error: false
            };
        case 'AUTH_FAIL':
            return state = {
                ...state,
                isLoading: false,
                error: action.payload
            };
        case '':
            return state = {

            };
        default:
            return state;
    }
}


export default Auth;