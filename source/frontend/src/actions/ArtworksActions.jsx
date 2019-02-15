// Local imports
import {
    artworksListAPI
} from '../actions/';


export function loadArtworks() {
    return (dispatch) => {
        dispatch(artworksListAPI());
    };
}

export function requestLoaded() {
    return {
        type: 'REQUEST_LOADED'
    };
}

export function inputError(error) {
    return {
        type: 'ERROR',
        payload: error
    };
}

export function setArtwork(input_id, input_data) {
    return {
        type: input_id,
        payload: input_data
    };
}

export function editArtwork(artworkToEdit) {
    return {
        type: 'EDIT_ARTWORK',
        payload: artworkToEdit
    };
}