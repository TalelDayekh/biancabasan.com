const defaultState = {
    allArtworksSorted: {},
    artworksSorting: true,
    // Toggle edit mode
    editMode: false,
    // User input
    inputErrors: [],
    formError: false,
    artworkId: '',
    title: '',
    yearFrom: '',
    yearTo: '',
    material: '',
    height: '',
    width: '',
    depth: '',
    description: '',
    images: []
}


const ArtworksAdmin = (state = defaultState, action) => {
    switch (action.type) {

        case 'LIST_ALL_ARTWORKS_SORTED':
            return state = {
                ...state,
                allArtworksSorted: action.payload
            }
        case 'SORT_SUCCESS':
            return state = {
                ...state,
                artworksSorting: false
            }
        case 'TOGGLE_EDIT_MODE':
            return state = {
                ...state,
                editMode: action.payload
            }
        
        // User input
        case 'SET_INPUT_ERRORS':
            return state = {
                ...state,
                inputErrors: action.payload
            }
        case 'SET_FORM_ERROR':
            return state = {
                ...state,
                formError: action.payload
            }
        case 'SET_ID':
            return state = {
                ...state,
                artworkId: action.payload
            }
        case 'SET_TITLE':
            return state = {
                ...state,
                title: action.payload
            }
        case 'SET_YEAR_FROM':
            return state = {
                ...state,
                yearFrom: action.payload
            }
        case 'SET_YEAR_TO':
            return state = {
                ...state,
                yearTo: action.payload
            }
        case 'SET_MATERIAL':
            return state = {
                ...state,
                material: action.payload
            }
        case 'SET_HEIGHT':
            return state = {
                ...state,
                height: action.payload
            }
        case 'SET_WIDTH':
            return state = {
                ...state,
                width: action.payload
            }
        case 'SET_DEPTH':
            return state = {
                ...state,
                depth: action.payload
            }
        case 'SET_DESCRIPTION':
            return state = {
                ...state,
                description: action.payload
            }
        case 'SET_IMAGES':
            return state = {
                ...state,
                images: action.payload
            }
        case 'RESET_ARTWORK_INFO':
            return state = {
                ...state,
                artworkId: '',
                title: '',
                yearFrom: '',
                yearTo: '',
                material: '',
                height: '',
                width: '',
                depth: '',
                description: ''
            }

        default:
            return state
    }
}


export default ArtworksAdmin