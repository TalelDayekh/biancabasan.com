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





// // // Axios
// // import axios from 'axios';

// // Set axios to accept token in header from sessionStorage
// export function createArtwork() {
//     return (dispatch, getState) => {
//         // Add authorization token to headers
//         let auth_state = getState().Auth;
//         const token = sessionStorage.getItem('token')
//         // const config = {
//         //     headers: {
//         //         'Content-Type': 'application/json'
//         //     }
//         // }
//         // if (token) {
//         //     config.headers['Authorization'] = `token ${token}`;
//         // }
//         axios.defaults.headers.common['Authorization'] = `token ${token}`;
//         // Create new artwork info and images
//         let artwork_state = getState().Artwork;
//         axios.post('http://127.0.0.1:8000/add_artwork_info/', {
//             title: artwork_state.title,
//             year_from: artwork_state.yearFrom,
//             year_to: artwork_state.yearTo,
//             material: artwork_state.material,
//             height: artwork_state.height,
//             width: artwork_state.width,
//             depth: artwork_state.depth,
//             description: artwork_state.description
//         }).then(res => {
//             // dispatch({
//             //     type: 'ADD_ID',
//             //     payload: res.data.id
//             // });

//             // (async function createImages() {
//             //     artwork_state = getState().Artwork;
//             //     const imageUploadForm = new FormData();
//             //     for (let i = 0; i < artwork_state.imageList.length; i++) {
//             //         const imageFile = artwork_state.imageList[i];
//             //         imageUploadForm.set('artwork_info', artwork_state.artworkObjectId);
//             //         imageUploadForm.append('image', imageFile);
//             //         await axios.post('http://127.0.0.1:8000/add_artwork_images/', imageUploadForm, {
//             //             headers: { 'content-type': 'multipart/form-data' }
//             //         });
//             //     }
//             // })();
//             dispatch({
//                 type: 'RESET_ARTWORK_STATE'
//             });
//             dispatch({
//                 type: 'ADMIN_MAIN',
//                 payload: true
//             })
//         }).catch(error => {
//             console.log(error)
//         })
//     }
// }