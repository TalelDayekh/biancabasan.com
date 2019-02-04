const defaultState = {
    toAdminMain: false,
    toAdminTitle: false,
    toAdminDetails: false,
    toAdminImages: false
}


const Redirect = (state = defaultState, action) => {
    switch (action.type) {
        case 'ADMIN_MAIN':
            return state = {
                ...state,
                toAdminMain: action.payload
            };
        case 'ADMIN_TITLE':
            return state = {
                ...state,
                toAdminTitle: action.payload
            };
        case 'ADMIN_DETAILS':
            return state = {
                ...state,
                toAdminDetails: action.payload
            };
        case 'ADMIN_IMAGES':
            return state = {
                ...state,
                toAdminImages: action.payload
            };
        case 'RESET_REDIRECT_STATE':
            return state = {
                ...state,
                toAdminMain: false,
                toAdminTitle: false,
                toAdminDetails: false,
                toAdminImages: false
            };
        default:
            return state;
    }
}


export default Redirect;