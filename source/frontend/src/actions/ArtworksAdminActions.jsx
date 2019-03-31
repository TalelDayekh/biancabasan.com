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
    return {
        type: inputFieldId,
        payload: inputData
    }
}

// Add uploaded image files to the images array
export function prepareImageUpload(imageFile) {
    return (dispatch, getState) => {
        const oldImagesArray = getState().ArtworksAdmin.images
        let newImagesArray = [ ...oldImagesArray ]

        newImagesArray.push(imageFile)

        dispatch({
            type: 'SET_IMAGES',
            payload: newImagesArray
        })
    }
}

//
export function removeImageFromUpload(imageIndex) {
    return (dispatch, getState) => {
        const artworkDetails = getState().ArtworksAdmin
        const oldImagesArray = getState().ArtworksAdmin.images
        let newImagesArray = [ ...oldImagesArray ]

        if (artworkDetails.artworkId) {
            console.log('The artwork has an id. Delete it from the db')
        } else {
            newImagesArray.splice(imageIndex, 1)
            console.log('The artwork has no id. Remove it from state')
        }

        dispatch({
            type: 'SET_IMAGES',
            payload: newImagesArray
        })
    }
}

// Find relevant artwork for edit based on id when edit
// mode is true and dispatch all info about the artwork
// to state.
export function toggleEditMode(editMode, artworkId) {
    return (dispatch, getState) => {
        dispatch({
            type: 'TOGGLE_EDIT_MODE',
            payload: editMode
        })

        if (artworkId) {
            Object.values(getState().ArtworksViews.allArtworks).forEach((artwork) => {
                const artworkForEdit = artwork.find(
                    findArtwork => findArtwork.id === artworkId
                )

                if (artworkForEdit) {
                    const artworkInfoState = {
                        SET_ID: artworkForEdit.id,
                        SET_TITLE: artworkForEdit.title,
                        SET_YEAR_FROM: artworkForEdit.year_from,
                        SET_YEAR_TO: artworkForEdit.year_to,
                        SET_MATERIAL: artworkForEdit.material,
                        SET_HEIGHT: artworkForEdit.height,
                        SET_WIDTH: artworkForEdit.width,
                        SET_DEPTH: artworkForEdit.depth,
                        SET_DESCRIPTION: artworkForEdit.description

                    }

                    for (let [key, value] of Object.entries(artworkInfoState)) {
                        dispatch({
                            type: key,
                            payload: value
                        })
                    }
                }
            })
        } else {
            dispatch({
                type: 'RESET_ARTWORK_INFO'
            })
        }
    }
}