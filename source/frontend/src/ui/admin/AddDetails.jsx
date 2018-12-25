import React, { Component } from 'react';
import axios from 'axios';
import './Admin.css';
import {
    AdminContentWrapper,
    AdminHeading,
    ShortInputField,
    LongInputField,
} from '../elements/';
import { throws } from 'assert';


class AddDetails extends Component {

    state = {
        yearFrom: "",
        yearTo: "",
        // Input errors
        incorrectInput: new Set()
    }

    // Variables for input field placeholders
    yearFrom = "Created between YYYY";
    yearTo = "and YYYY*";


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
                            name = "yearFrom"
                            size = "1"
                            placeholder = { this.yearFrom }
                            onFocus = { this.clearPlaceholder }
                            onBlur = { this.formValidation }
                            value = { this.state.yearFrom }
                            onChange = { this.updateDetailsState }
                            raiseError = { this.state.incorrectInput.has('yearFrom') ? true : undefined }
                        />
                        <div className = "spacer-div-middle" />
                        <ShortInputField
                            name = "yearTo"
                            size = "1"
                            placeholder = { this.yearTo }
                            onFocus = { this.clearPlaceholder }
                            onBlur = { this.formValidation }
                            value = { this.state.yearTo }
                            onChange = { this.updateDetailsState }
                            raiseError = { this.state.incorrectInput.has('yearTo') ? true : undefined }
                        />
                    </div>
                </form>
            </AdminContentWrapper>
        )
    }


    updateDetailsState = (event) => {
        this.setState({
            [event.target.name]: event.target.value
        });

        let inputError = event.target.name;
        this.state.incorrectInput.delete(inputError) 
    }

    clearPlaceholder = (event) => {
        event.target.placeholder = ""
    }

    formValidation = (event) => {
        if (event.target.name === 'yearFrom') {
            if (this.state.yearFrom.length != 4 || isNaN(this.state.yearFrom)) {
                let updatedSet = this.state.incorrectInput.add('yearFrom');
                this.setState({
                    incorrectInput: updatedSet
                });
                event.target.placeholder = "PLACEHOLDER TEXT"
            }
        }

        if (event.target.name === 'yearTo') {
            if (this.state.yearTo.length != 4 || isNaN(this.state.yearTo)) {
                let updatedSet = this.state.incorrectInput.add('yearTo');
                this.setState({
                    incorrectInput: updatedSet
                });
                event.target.placeholder = "PLACEHOLDER TEXT"
            }
        }
    }

}


export default AddDetails;