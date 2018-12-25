import React, { Component } from 'react';
import axios from 'axios';
import './Admin.css';
import {
    AdminContentWrapper,
    AdminHeading,
    ShortInputField,
    LongInputField,
    TextField,
    SaveButton,
    BackButton
} from '../elements/';


class AddDetails extends Component {

    state = {
        yearFrom: "",
        yearTo: "",
        material: "",
        height: "",
        width: "",
        depth: "",
        description: "",
        // Input errors
        incorrectInput: new Set()
    }

    // Variables for input field placeholders
    yearFrom = "Created between YYYY*"
    yearTo = "and YYYY*"
    material = "Material*"
    height = "Height*"
    width = "Width*"
    depth = "Depth"
    description = "Description*"


    render = () => {
        return(
            <AdminContentWrapper>
                {/* Heading */}
                <AdminHeading>
                    Add some specs and describe your work a bit
                </AdminHeading>

                <form>
                    {/* Input fields */}
                    {/* Years */}
                    <div className = "years-flex-container">
                        <ShortInputField
                            id = "yearFrom"
                            name = "years"
                            size = "1"
                            placeholder = { this.yearFrom }
                            onFocus = { this.clearPlaceholder }
                            onBlur = { this.inputValidation }
                            value = { this.state.yearFrom }
                            onChange = { this.updateDetailsState }
                            raiseError = { this.state.incorrectInput.has('yearFrom') ? true : undefined }
                        />
                        <div className = "spacer-div-middle"/>
                        <ShortInputField
                            id = "yearTo"
                            name = "years"
                            size = "1"
                            placeholder = { this.yearTo }
                            onFocus = { this.clearPlaceholder }
                            onBlur = { this.inputValidation }
                            value = { this.state.yearTo }
                            onChange = { this.updateDetailsState }
                            raiseError = { this.state.incorrectInput.has('yearTo') ? true : undefined }
                        />
                    </div>
                    {/* Material */}
                    <div className = "input-flex-container">
                        <LongInputField
                            id = "material"
                            name = "text"
                            size = "1"
                            placeholder = { this.material }
                            onFocus = { this.clearPlaceholder }
                            onBlur = { this.inputValidation }
                            value = { this.state.material }
                            onChange = { this.updateDetailsState }
                            raiseError = { this.state.incorrectInput.has('material') ? true : undefined }
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
                            value = { this.state.height }
                            onChange = { this.updateDetailsState }
                            raiseError = { this.state.incorrectInput.has('height') ? true : undefined }
                        />
                        <div className = "spacer-div-right"/>
                    </div>
                    {/* Width */}
                    <div className = "input-flex-container">
                        <ShortInputField
                            id = "width"
                            name = "numbers"
                            size = "1"
                            placeholder = { this.width }
                            onFocus = { this.clearPlaceholder }
                            onBlur = { this.inputValidation }
                            value = { this.state.width }
                            onChange = { this.updateDetailsState }
                            raiseError = { this.state.incorrectInput.has('width') ? true : undefined }
                        />
                        <div className = "spacer-div-right"/>
                    </div>
                    {/* Depth */}
                    <div className = "input-flex-container">
                        <ShortInputField
                            id = "depth"
                            name = "numbers"
                            size = "1"
                            placeholder = { this.depth }
                            onFocus = { this.clearPlaceholder }
                            onBlur = { this.inputValidation }
                            value = { this.state.depth }
                            onChange = { this.updateDetailsState }
                            raiseError = { this.state.incorrectInput.has('depth') ? true : undefined }
                        />
                        <div className = "spacer-div-right"/>
                    </div>
                    {/* Description */}
                    <div className = "input-flex-container">
                        <TextField
                            id = "description"
                            name = "text"
                            size = "1"
                            placeholder = { this.description }
                            onFocus = { this.clearPlaceholder }
                            onBlur = { this.inputValidation }
                            value = { this.state.description }
                            onChange = { this.updateDetailsState }
                            raiseError = { this.state.incorrectInput.has('description') ? true : undefined }
                        />
                    </div>

                    {/* Buttons */}
                    <SaveButton>Save</SaveButton>
                    <BackButton>Back</BackButton>
                </form>
            </AdminContentWrapper>
        )
    }


    updateDetailsState = (event) => {
        this.setState({
            [event.target.id]: event.target.value
        });

        let inputError = event.target.id;
        this.state.incorrectInput.delete(inputError) 
    }

    clearPlaceholder = (event) => {
        event.target.placeholder = ""
    }

    inputValidation = (event) => {
        let inputId = event.target.id

        if (event.target.name === 'years') {
            if(this.state[inputId].length != 4 || isNaN(this.state[inputId])) {
                let updatedSet = this.state.incorrectInput.add(inputId);
                this.setState({
                    incorrectInput: updatedSet
                });
                event.target.placeholder = "PLACEHOLDER TEXT"
            }
        }
        if (event.target.name === 'numbers') {
            if(this.state[inputId].length === 0 || isNaN(this.state[inputId])) {
                let updatedSet = this.state.incorrectInput.add(inputId);
                this.setState({
                    incorrectInput: updatedSet
                });
                event.target.placeholder = "PLACEHOLDER TEXT"
            }
        }
        if (event.target.name === 'text') {
            if(this.state[inputId].length === 0) {
                let updatedSet = this.state.incorrectInput.add(inputId);
                this.setState({
                    incorrectInput: updatedSet
                });
                event.target.placeholder = "PLACEHOLDER TEXT"
            }
        }
    }

}


export default AddDetails;