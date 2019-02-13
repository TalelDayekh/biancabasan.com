const defaultState = {
    // Pages redirect
    toAdminMain: false,
    toAdminTitle: false,
    toAdminDetails: false,
    toAdminImages: false,
    // Pages edit mode
    editMode: false
}


const Redirect = (state = defaultState, action) => {
    switch (action.type) {
        // Pages redirect
        case 'ADMIN_MAIN':
            return state = {
                ...state,
                toAdminMain: true
            };
        case 'ADMIN_TITLE':
            return state = {
                ...state,
                toAdminTitle: true
            };
        case 'ADMIN_DETAILS':
            return state = {
                ...state,
                toAdminDetails: true
            };
        case 'ADMIN_IMAGES':
            return state = {
                ...state,
                toAdminImages: true
            };
        // Pages edit mode
        case 'EDIT_MODE':
            return state = {
                ...state,
                editMode: action.payload
            };
        // Reset- and default state
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