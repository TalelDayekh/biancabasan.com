// Axios
import axios from 'axios'
// Local imports
import {
    artworksLoaded,
    listArtworks,
    listYears,
    artworksLoadingError
} from '../actions/'


// Get artwork objects, filter them by year and add to a new object
// with years as keys and an array of the initial objects as values.
// Then add each year to an array and sort descending.
export function readArtworksAPI() {
    return (dispatch) => {
        axios.get('http://localhost:8000/all_artworks')
        .then(res => {
            let allArtworks = {}
            res.data.forEach((artwork) => {
                let year = artwork.year_to
                allArtworks[year] = res.data.filter(artwork => artwork.year_to === year)
            })

            const artworksYears = Object.keys(allArtworks)
            let allYears = [ ...artworksYears ]
            allYears.sort((a, b) => b - a)

            dispatch(listArtworks(allArtworks))
            dispatch(listYears(allYears))
            dispatch(artworksLoaded())
        })
        .catch(error => {
            dispatch(artworksLoadingError(error))
        })
    }
}