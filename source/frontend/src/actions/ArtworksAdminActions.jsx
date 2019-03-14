// Create a new object for allArtworks where each year has
// an array of artwork objects sorted descendingly by id.
export function loadSortedArtworks() {
    return (dispatch, getState) => {
        let newAllArtworksObject = { ...getState().ArtworksViews.allArtworks }

        Object.keys(newAllArtworksObject).forEach((year) => {
            newAllArtworksObject[year].sort((a, b) => b.id - a.id)
        })

        dispatch({
            type: 'LIST_ALL_ARTWORKS_SORTED',
            payload: newAllArtworksObject
        })
        dispatch({
            type: 'SORT_SUCCESS'
        })
    }
}

// Handle user input errors by adding and removing the
// id value of input fields to and from an array.
export function setInputErrors(inputError, errorField) {
    return (dispatch, getState) => {
        let newInputErrorsArray = [ ...getState().ArtworksAdmin.inputErrors ]

        if (inputError) {
            if (newInputErrorsArray.indexOf(errorField) === -1) {
                newInputErrorsArray.push(errorField)
            }

            dispatch({
                type: 'SET_INPUT_ERRORS',
                payload: newInputErrorsArray
            })
        } else if (!(inputError)) {
            let deletedErrorsArray = newInputErrorsArray.filter(error => error !== errorField)

            dispatch({
                type: 'SET_INPUT_ERRORS',
                payload: deletedErrorsArray
            })
        }
    }
}

export function setFormError(error) {
    return {
        type: 'SET_FORM_ERROR',
        payload: error
    }
}

//
export function setArtwork(inputFieldId, inputData) {
    return (dispatch, getState) => {
        dispatch({
            type: inputFieldId,
            payload: inputData
        })
    }
}

export function toggleEditMode(editMode, artworkId) {
    return (dispatch) => {
        dispatch({
            type: 'TOGGLE_EDIT_MODE',
            payload: editMode
        })
        if (artworkId) {
            dispatch({
                type: 'SET_ID',
                payload: artworkId
            })
        } else {
            dispatch({
                type: 'SET_ID',
                payload: ''
            })
            dispatch({
                type: 'SET_ARTWORK_FOR_EDIT',
                payload: {}
            })
        }
    }
}

// Find relevant artwork for edit based on id 
// and dispatch the artwork object to state.
export function loadArtworkForEdit() {
    return (dispatch, getState) => {
        Object.values(getState().ArtworksViews.allArtworks).forEach((artwork) => {
            const artworkForEdit = artwork.find(
                findArtwork => findArtwork.id === getState().ArtworksAdmin.artworkId
            )
            if (artworkForEdit) {
                dispatch({
                    type: 'SET_ARTWORK_FOR_EDIT',
                    payload: artworkForEdit
                })
            }
        })
    }
}