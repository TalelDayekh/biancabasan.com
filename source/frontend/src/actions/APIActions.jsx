// Axios
import axios from 'axios';
// Local imports
import {
    authSuccess,
    authFail,
    requestLoaded
} from '../actions';


export function loginAPI(username, password) {
    return (dispatch) => {
        axios.post('http://localhost:8000/auth/login/', {
            username: username,
            password: password
        }).then(res => {
            const token = res.data.key;
            sessionStorage.setItem('token', token);
            dispatch(authSuccess());
        }).catch(error => {
            dispatch(authFail(error));
        })
    }
}

export function artworksListAPI() {
    return (dispatch) => {
        axios.get('http://localhost:8000/all_artworks').then(res => {
            let allArtworks = {}
            res.data.forEach((obj) => {
                let year = obj.year_to;
                allArtworks[year] = res.data.filter(artwork => artwork.year_to === year)
            });
            dispatch({
                type: 'LIST_ARTWORKS',
                payload: allArtworks
            });
            dispatch(requestLoaded());
        })
    }
}

export function createArtworkAPI() {
    return (dispatch, getState) => {
        // Add authorization token to headers
        axios.defaults.headers.common['Authorization'] = `token ${sessionStorage.getItem('token')}`;
        let artworkInfo = getState().Artwork;
        // Create title and details
        axios.post('http://localhost:8000/add_artwork_info/', {
            title: artworkInfo.title,
            year_from: artworkInfo.yearFrom,
            year_to: artworkInfo.yearTo,
            material: artworkInfo.material,
            height: artworkInfo.height,
            width: artworkInfo.width,
            depth: artworkInfo.depth,
            description: artworkInfo.description
        }).then(res => {
            dispatch({
                type: 'SET_ID',
                payload: res.data.id
            });
            // Create images
            (async function createImagesAPI() {
                let artworkInfo = getState().Artwork
                let imageUploadForm = new FormData();
                for (let i = 0; i < artworkInfo.imageList.length; i++) {
                    let imageFile = artworkInfo.imageList[i];
                    imageUploadForm.set('artwork_info', artworkInfo.artworkObjectId);
                    imageUploadForm.append('image', imageFile);
                    await axios.post('http://localhost:8000/add_artwork_images/', imageUploadForm, {
                        headers: { 'content-type': 'multipart/form-data' }
                    });
                }
            })();
            dispatch({
                type: 'RESET_ARTWORK_STATE'
            });
            dispatch({
                type: 'ADMIN_MAIN',
                payload: true
            });
        }).catch(error => {
            console.log('ERROR!') // !! ADD ERROR TO ARTWORKS REDUCERS
        });
    }
}