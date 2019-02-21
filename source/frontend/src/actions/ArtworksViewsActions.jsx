// Add artworks to pagination object
export function addArtworksToPagination(artworksYear, artworksArray) {
    return (dispatch, getState) => {
        let oldPaginationObject = getState().ArtworksViews.pagination
        let newPaginationObject = { ...oldPaginationObject }

        newPaginationObject[artworksYear] = artworksArray

        dispatch({
            type: 'ARTWORKS_TO_PAGINATION',
            payload: newPaginationObject
        })
    }
}

// Set no. of years as iteration counter
export function yearsTotal(yearsCount) {
    return (dispatch) => {
        // Start counting from the object's second value
        const years = -1 + yearsCount

        dispatch({
            type: 'YEARS_TO_ITERATIONS',
            payload: years
        })
    }
}