import React, { Component } from 'react'
// Local imports
// Elements
import {
    ShortInputField,
    LongInputField,
    TextField
} from '../elements/'


class DetailsForm extends Component {

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
                <form>
                    <div>
                        <ShortInputField
                            id='SET_YEAR_FROM'
                            name='years'
                            size='1'
                            placeholder={ this.yearFrom }
                            onFocus={ this.clearPlaceholder }
                            onBlur={ (e) => {this.inputValidation(e); this.errorCheck(e)} }

                            onChange={ (e) => {this.props.setArtwork(e)} }
                            // raiseError={ customAttribute }
                        />
                        <ShortInputField
                            id='SET_YEAR_TO'
                            name='years'
                            size='1'
                            placeholder={ this.yearTo }
                            onFocus={ this.clearPlaceholder }
                            onBlur={ this.inputValidation }

                            onChange={ (e) => {this.props.setArtwork(e)} }
                            raiseError={ this.props.admin.formValidationError ? true : undefined }
                        />
                    </div>
                    <div>
                        <LongInputField
                            id='SET_MATERIAL'
                            name='text'
                            size='1'
                            placeholder={ this.material }
                            onFocus={ this.clearPlaceholder }
                            onBlur={ this.inputValidation }

                            onChange={ (e) => {this.props.setArtwork(e)} }
                            raiseError={ this.props.admin.formValidationError ? true : undefined }
                        />
                    </div>
                    <div>
                        <ShortInputField
                            id='SET_HEIGHT'
                            name='measurement'
                            size='1'
                            placeholder={ this.height }
                            onFocus={ this.clearPlaceholder }
                            onBlur={ this.inputValidation }

                            onChange={ (e) => {this.props.setArtwork(e)} }
                            raiseError={ this.props.admin.formValidationError ? true : undefined }
                        />
                    </div>
                    <div>
                        <ShortInputField
                            id='SET_WIDTH'
                            name='measurement'
                            size='1'
                            placeholder={ this.width }
                            onFocus={ this.clearPlaceholder }
                            onBlur={ this.inputValidation }

                            onChange={ (e) => {this.props.setArtwork(e)} }
                            raiseError={ this.props.admin.formValidationError ? true : undefined }
                        />
                    </div>
                    <div>
                        <ShortInputField
                            id='SET_DEPTH'
                            name='measurement'
                            size='1'
                            placeholder={ this.depth }
                            onFocus={ this.clearPlaceholder }
                            onBlur={ this.inputValidation }

                            onChange={ (e) => {this.props.setArtwork(e)} }
                            raiseError={ this.props.admin.formValidationError ? true : undefined }
                        />
                    </div>
                    <div>
                        <TextField
                            id='SET_DESCRIPTION'
                            name='text'
                            size='1'
                            placeholder={ this.description }
                            onFocus={ this.clearPlaceholder }
                            onBlur={ this.inputValidation }

                            onChange={ (e) => {this.props.setArtwork(e)} }
                            raiseError={ this.props.admin.formValidationError ? true : undefined }
                        />
                    </div>
                </form>
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
        // seperated by either perios or comma. Except for the depth
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

}


export default DetailsForm