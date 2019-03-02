// Local imports
import {
    readArtworksAPI
} from '../actions/'


export function loadArtworks() {
    return (dispatch) => {
        dispatch(readArtworksAPI())
    }
}

export function artworksLoaded() {
    return {
        type: 'LOAD_SUCCESS'
    }
}

export function artworksLoadingError(error) {
    return {
        type: 'LOAD_FAIL',
        payload: error
    }
}

export function listArtworks(allArtworks) {
    return {
        type: 'LIST_ALL_ARTWORKS',
        payload: allArtworks
    }
}

export function listYears(allYears) {
    return {
        type: 'LIST_ALL_YEARS',
        payload: allYears
    }
}

// Take in a year from the allYears array
// and add it to the pagination array.
export function addYearToPagination(year) {
    return (dispatch, getState) => {
        let oldYearsPaginationArray = getState().ArtworksViews.yearsPagination
        let newYearsPaginationArray = [ ...oldYearsPaginationArray ]

        // Prevents from adding null values
        if (year) {
            newYearsPaginationArray.push(year)
        }

        dispatch({
            type: 'YEAR_TO_PAGINATION',
            payload: newYearsPaginationArray
        })
    }
}

// Take in a year and retrieve all relevant artworks for that year. Sort them
// descendingly by id and add the artwork for the current iteration to a copy
// of the artworksPagination object in an array that is a value for the year.
// Sort the array of artworks descendingly by id before dispatch.
export function addArtworkToPagination(year, artworksCurrentIteration) {
    return (dispatch, getState) => {
        const allArtworksForYear = getState().ArtworksViews.allArtworks[year]
        allArtworksForYear.sort((a, b) => b.id - a.id)
        const artworkForCurrentIteration = allArtworksForYear[artworksCurrentIteration]

        let oldArtworksPaginationObject = getState().ArtworksViews.artworksPagination
        let newArtworksPaginationObject = { ...oldArtworksPaginationObject }

        // If the year already exists in the artworksPagination object then push
        // the artwork for the current iteration to the array for that year. If
        // the year doesn't exist add it to the artworksPagination object as key
        // and add an array with the artwork for the current iteration as value.
        if (newArtworksPaginationObject[year]) {
            newArtworksPaginationObject[year].push(artworkForCurrentIteration) 
        } else {
            newArtworksPaginationObject[year] = [artworkForCurrentIteration]
        }

        newArtworksPaginationObject[year].sort((a, b) => b.id - a.id)

        dispatch({
            type: 'ARTWORK_TO_PAGINATION',
            payload: newArtworksPaginationObject
        })
    }
}