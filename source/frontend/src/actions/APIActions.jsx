// Axios
import axios from 'axios';


export function createArtwork() {
    let state
    return (dispatch, getState) => {
        state = getState().Artwork;
        axios.post('http://localhost:8000/add_artwork_info/', {
            owner: 1, // !! REMOVE HARD CODED OWNER !!
            title: state.title,
            year_from: state.yearFrom,
            year_to: state.yearTo,
            material: state.material,
            height: state.height,
            width: state.width,
            depth: state.depth,
            description: state.description
        }).then(res => {
            dispatch({
                type: 'ADD_ID',
                payload: res.data.id
            });

            (async function createImages() {
                state = getState().Artwork;
                const imageUploadForm = new FormData();
                for (let i = 0; i < state.imageList.length; i++) {
                    const imageFile = state.imageList[i];
                    imageUploadForm.set('artwork_info', state.artworkObjectId);
                    imageUploadForm.append('image', imageFile);
                    await axios.post('http://localhost:8000/add_artwork_images/', imageUploadForm, {
                        headers: { 'content-type': 'multipart/form-data' }
                    });
                }
            })();
            dispatch({
                type: 'RESET_ARTWORK_STATE'
            })
        })
    }
}