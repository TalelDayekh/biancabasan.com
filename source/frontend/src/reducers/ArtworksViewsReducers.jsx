const defaultState = {
    pagination: {},
    // Total amount of available years to iterate
    // when adding new artworks to pagination.
    totalIterations: null
}


const ArtworksViews = (state = defaultState, action) => {
    switch (action.type) {

        case 'ARTWORKS_TO_PAGINATION':
            return state = {
                ...state,
                pagination: action.payload
            }
        case 'YEARS_TO_ITERATIONS':
            return state = {
                ...state,
                totalIterations: action.payload
            }

        default:
            return state
    }
}


export default ArtworksViews