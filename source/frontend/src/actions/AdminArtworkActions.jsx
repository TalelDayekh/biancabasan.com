export function setArtwork(input_id, input_data) {
    return {
        type: input_id,
        payload: input_data
    };
}

export function inputError(error) {
    return {
        type: 'ERROR',
        payload: error
    }
}