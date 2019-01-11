import React, { Component } from 'react';
import './Admin.css';
import {
    LongInputField,
    ShortInputField,
    TextField,
    SaveButton,
    BackButton
} from '../elements/';


class DetailsForm extends Component {

    state = {
        yearFrom: "",
        yearTo: "",
        material: "",
        height: "",
        width: "",
        depth: "",
        description: "",
        // Edit mode
        editDetailsMode: false,
        // Input errors
        incorrectInput: new Set()
    }

    // Variables for input field placeholders
    yearFrom = "Created from YYYY"
    yearTo = "to YYYY*"
    material = "Material*"
    height = "Height*"


    // Change state based on props
    // to prepare form for edit mode
    static getDerivedStateFromProps = (props, state) => {
        if (props.editMode != state.editDetailsMode) {
            return {
                editDetailsMode: props.editMode,
                yearFrom: props.retrievedDetails.year_from,
                yearTo: props.retrievedDetails.year_to,
                material: props.retrievedDetails.material,
                height: props.retrievedDetails.height,
                width: props.retrievedDetails.width,
                depth: props.retrievedDetails.depth,
                description: props.retrievedDetails.description
            };
        }
        return null;
    }

    render = () => {
        return(
            <form>
                {/* Input fields */}
                {/* Years */}
                <div className = "top-input-flex-container">
                    <ShortInputField
                        id = "yearFrom"
                        name = "nullYear"
                        size = "1"
                        placeholder = { this.yearFrom }
                        onFocus = { this.clearPlaceholder }
                        onBlur = { this.inputValidation }
                        defaultValue = { this.state.editDetailsMode ? 
                            this.props.retrievedDetails.year_from : 
                            this.state.yearFrom }
                        onChange = { this.updateDetailsState }
                    />
                    <div className = "spacer-div-middle" />
                    <ShortInputField
                        id = "yearTo"
                        name = "years"
                        size = "1"
                        placeholder = { this.yearTo }
                        onFocus = { this.clearPlaceholder }
                        onBlur = { this.inputValidation }
                        defaultValue = { this.state.editDetailsMode ? 
                            this.props.retrievedDetails.year_to : 
                            this.state.yearTo }
                        onChange = { this.updateDetailsState }
                        raiseError = { this.state.incorrectInput.has('yearTo') ? true : undefined }
                    />
                </div>
                {/* Material */}
                <div className = "input-flex-container">
                    <LongInputField
                        id = "material"
                        name = "nullText"
                        size = "1"
                        placeholder = { this.material }
                        onFocus = { this.clearPlaceholder }
                        onBlur = { this.inputValidation }
                        defaultValue = { this.state.editDetailsMode ? 
                            this.props.retrievedDetails.material : 
                            this.state.material }
                        onChange = { this.updateDetailsState }
                    />
                </div>
                {/* Height */}
                <div className = "input-flex-container">
                    <ShortInputField
                        id = "height"
                        name = "numbers"
                        size = "1"
                        placeholder = { this.height }
                        onFocus = { this.clearPlaceholder }
                        onBlur = { this.inputValidation }
                        defaultValue = { this.state.editDetailsMode ? 
                            this.props.retrievedDetails.height : 
                            this.state.height }
                        onChange = { this.updateDetailsState }
                        raiseError = { this.state.incorrectInput.has('height') ? true : undefined }
                    />
                    <div className = "spacer-div-right" />
                </div>
                {/* Width */}
                <div className = "input-flex-container">
                    <ShortInputField
                    />
                    <div className = "spacer-div-right" />
                </div>
            </form>
        )
    }


    updateDetailsState = (e) => {
        this.setState({
            [e.target.id]: e.target.value
        });

        let inputError = e.target.id;
        this.state.incorrectInput.delete(inputError)
    }

    clearPlaceholder = (e) => {
        e.target.placeholder = ""
    }

    inputValidation = (e) => {
        let inputId = e.target.id

        // Validate year inputs
        if (e.target.name === "nullYear") {
            if (e.target.value.length != 4 || isNaN(this.state[inputId])) {
                this.setState({
                    [inputId]: ""
                });
            }
            if (e.target.value.length === 0) {
                e.target.placeholder = this.yearFrom
            }
        }
        if (e.target.name === "years") {
            if (e.target.value.length != 4 || isNaN(this.state[inputId])) {
                let updatedErrorSet = this.state.incorrectInput.add(inputId);
                this.setState({
                    incorrectInput: updatedErrorSet
                });
                e.target.placeholder = "ERROR TEXT"
            }
        }

        // Validate text inputs
        if (e.target.name === "nullText") {
            if (e.target.value.length === 0) {
                e.target.placeholder = this.material
            }
        }
        if (e.target.name === "text") {
            if (e.target.value.length === 0) {
                let updatedErrorSet = this.state.incorrectInput.add(inputId);
                this.setState({
                    incorrectInput: updatedErrorSet
                });
                e.target.placeholder = "ERROR TEXT"
            }
        }

        // Validate measurement inputs
        if (e.target.name === "numbers") {
            if (e.target.value.length === 0 || isNaN(this.state[inputId])) {
                let updatedErrorSet = this.state.incorrectInput.add(inputId);
                this.setState({
                    incorrectInput: updatedErrorSet
                });
                e.target.placeholder = "ERROR TEXT"
            }
        }
    }
}


export default DetailsForm;