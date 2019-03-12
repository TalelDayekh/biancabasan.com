const defaultState = {
    toAdminMain: false,
    toAdminTitle: false,
    toAdminDetails: false,
    toAdminImages: false
}


const AdminRedirect = (state = defaultState, action) => {
    switch (action.type) {
        case 'ADMIN_MAIN':
            return state = {
                ...state,
                toAdminMain: !state.toAdminMain
            }
        case 'ADMIN_TITLE':
            return state = {
                ...state,
                toAdminTitle: !state.toAdminTitle
            }
        case 'ADMIN_DETAILS':
            return state = {
                toAdminDetails: !state.toAdminDetails
            }
        case 'ADMIN_IMAGES':
            return state = {
                ...state,
                toAdminImages: !state.toAdminImages
            }
        
        default:
            return state
    }
}


export default AdminRedirect