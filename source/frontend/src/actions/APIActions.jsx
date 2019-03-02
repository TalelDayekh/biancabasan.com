// Axios
import axios from 'axios'
// Local imports
import {
    artworksLoaded,
    listArtworks,
    listYears,
    artworksLoadingError,
    authenticationSuccess,
    loginFailError
} from '../actions/'


// Get artwork objects, filter them by year and add to a new object
// with years as keys and an array of the initial objects as values.
// Then add each year to an array and sort descendingly.
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

// Tries a user's input for username and password against users
// in the database and retrieves a key if there is a match. The
// key is stored in sessionStorage as a token for that user. 
export function userLoginAPI(username, password) {
    return (dispatch) => {
        axios.post('http://localhost:8000/auth/login/', {
            username: username,
            password: password
        })
        .then(res => {
            const token = res.data.key
            sessionStorage.setItem('token', token)
            dispatch(authenticationSuccess())
        })
        .catch(error => {
            dispatch(loginFailError(error))
        })
    }
}