export function setArtwork(input_id, input_data) {
    return {
        type: input_id,
        payload: input_data
    };
}