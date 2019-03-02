const defaultState = {
    allArtworks: {},
    allYears: [],
    artworksLoading: true,
    loadingError: false,
    yearsPagination: [],
    artworksPagination: {}
}


const ArtworksViews = (state = defaultState, action) => {
    switch (action.type) {

        case 'LIST_ALL_ARTWORKS':
            return state = {
                ...state,
                allArtworks: action.payload
            }
        case 'LIST_ALL_YEARS':
            return state = {
                ...state,
                allYears: action.payload
            }
        case 'LOAD_SUCCESS':
            return state = {
                ...state,
                artworksLoading: false,
                loadingError: false
            }
        case 'LOAD_FAIL':
            return state = {
                ...state,
                loadingError: true
            }
        case 'YEAR_TO_PAGINATION':
            return state = {
                ...state,
                yearsPagination: action.payload
            }
        case 'ARTWORK_TO_PAGINATION':
            return state = {
                ...state,
                artworksPagination: action.payload
            }

        default:
            return state
    }
}


export default ArtworksViews