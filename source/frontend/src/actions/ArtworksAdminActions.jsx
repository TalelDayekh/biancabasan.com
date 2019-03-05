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
            if (!(newInputErrorsArray.includes(errorField))) {
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