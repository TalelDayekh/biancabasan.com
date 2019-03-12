import React, { Component } from 'react'
// Local imports
// Elements
import {
    ShortInputField,
    LongInputField,
    TextField,
    NextButton,
    BackButton
} from '../elements/'


const formFields = [
    {id: 'SET_YEAR_FROM', name: 'years', inputField: 'yearFrom'},
    {id: 'SET_YEAR_TO', name: 'years', inputField: 'yearTo'},
    {id: 'SET_MATERIAL', name: 'text', inputField: 'material'},
    {id: 'SET_HEIGHT', name: 'measurement', inputField: 'height'},
    {id: 'SET_WIDTH', name: 'measurement', inputField: 'width'},
    {id: 'SET_DEPTH', name: 'measurement', inputField: 'depth'},
    {id: 'SET_DESCRIPTION', name: 'text', inputField: 'description'}
]


class DetailsForm extends Component {

    // Variables for input field placeholders
    yearFrom='Created between YYYY*'
    yearTo='and YYYY*'
    material='Material*'
    height='Height*'
    width='Width*'
    depth='Depth'
    description='Description*'

    render = () => {
        return(
            <React.Fragment>
                <form id='next' onSubmit={ this.errorCheck }>
                    {
                        formFields.map((formField, i) => {
                            if ((formField.name==='years') || (formField.name==='measurement')) {
                                return(
                                    <div key={i}>
                                        <ShortInputField
                                            id={ formField.id }
                                            name={ formField.name }
                                            size='1'
                                            placeholder={ this[formField.inputField] }
                                            onFocus={ this.clearPlaceholder }
                                            onBlur={ this.inputValidation }

                                            onChange={ (e) => {this.props.setArtwork(e)} }
                                            raiseError={ (this.props.admin.inputErrors.indexOf(formField.id) !== -1) ? true : undefined }
                                        />
                                    </div>
                                )
                            }
                            if ((formField.name==='text') && (!(formField.id==='SET_DESCRIPTION'))) {
                                return(
                                    <div key={i}>
                                        <LongInputField
                                            id={ formField.id }
                                            name={ formField.name }
                                            size='1'
                                            placeholder={ this[formField.inputField] }
                                            onFocus={ this.clearPlaceholder }
                                            onBlur={ this.inputValidation }

                                            onChange={ (e) => {this.props.setArtwork(e)} }
                                            raiseError={ (this.props.admin.inputErrors.indexOf(formField.id) !== -1) ? true : undefined }
                                        />
                                    </div>
                                )
                            }
                            else {
                                return(
                                    <div key={i}>
                                        <TextField
                                            id={ formField.id }
                                            name={ formField.name }
                                            size='1'
                                            placeholder={ this[formField.inputField] }
                                            onFocus={ this.clearPlaceholder }
                                            onBlur={ this.inputValidation }

                                            onChange={ (e) => {this.props.setArtwork(e)} }
                                            raiseError={ (this.props.admin.inputErrors.indexOf(formField.id) !== -1) ? true : undefined }
                                        />
                                    </div>
                                )
                            }
                        })
                    }
                    <NextButton type='submit'>Next</NextButton>
                </form>
                <BackButton id='back' onClick={ this.switchAdminPanel }>Back</BackButton>
            </React.Fragment>
        )
    }


    clearPlaceholder = (e) => {
        e.target.placeholder=''
        this.props.setInputErrors(false, e.target.id)
    }

    inputValidation = (e) => {
        // Raise error if user inputs anything
        // or nothing but four digits in a row.
        if (e.target.name==='years') {
            const RegEx=/^\d{4}$/

            if (!(e.target.value.match(RegEx))) {
                this.props.setInputErrors(true, e.target.id)
            }
        }
        // Raise error if user inputs nothing
        // or begins string with white space.
        if (e.target.name==='text') {
            const RegEx=/^\S.*/

            if (!(e.target.value.match(RegEx))) {
                this.props.setInputErrors(true, e.target.id)
            }
        }
        // Raise error if user inputs nothing or anything but digits
        // seperated by either period or comma. Except for the depth
        // field which accepts an empty string as value.
        if (e.target.name==='measurement') {
            const RegEx=/^\d*(.|,)?\d+$/

            if ((!(e.target.value.match(RegEx))) && (!(e.target.id==='SET_DEPTH'))) {
                this.props.setInputErrors(true, e.target.id)
            }
            if (((!(e.target.value.match(RegEx))) && (e.target.value.length !== 0)) && e.target.id==='SET_DEPTH') {
                this.props.setInputErrors(true, e.target.id)
            }

        }
    }

    // Catch if user input is not matching the requirements and
    // add all the faulty input fields to the inputErrors array.
    errorCheck = (e) => {
        e.preventDefault()
        
        try {
            formFields.forEach((formField) => {
                if (((this.props.admin[formField.inputField].length===0) && (!(formField.id==='SET_DEPTH'))) ||
                    (this.props.admin.inputErrors.indexOf(formField.id) !== -1)) {
                        throw new Error('Required input fields are either empty or'
                                        + ' have a faulty value')
                    }
            })
            this.switchAdminPanel(e)
        } catch(error) {
            formFields.forEach((formField) => {
                if(((this.props.admin[formField.inputField].length===0) && (!(formField.id==='SET_DEPTH'))) ||
                    (this.props.admin.inputErrors.indexOf(formField.id) !== -1)) {
                        this.props.setInputErrors(true, formField.id)
                    }
            })
        }
    }

    switchAdminPanel = (e) => {
        this.props.switchAdminPanel(e)
    }
    
}


export default DetailsForm