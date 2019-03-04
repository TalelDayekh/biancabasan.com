import React, { Component } from 'react'
// Local imports
// Elements
import {
    ShortInputField,
    LongInputField,
    TextField
} from '../elements/'


class DetailsForm extends Component {

    // Variables for input field placeholders
    yearFrom='Created between YYYY'
    yearTo='and YYYY*'

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
                            onBlur={ this.inputValidation }

                            onChange={ (e) => {this.props.setArtwork(e)} }
                            raiseError={ this.props.admin.formValidationError ? true : undefined }
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
                </form>
            </React.Fragment>
        )
    }


    clearPlaceholder = (e) => {
        e.target.placeholder=''
        // this.props.setFormError(false)
    }

    //
    inputValidation = (e) => {
        if (e.target.name === 'years') {
            const RegEx = /^\d{4}$/
            if (!(this.props.admin.yearFrom.match(RegEx))) {
                // this.props.setFormError(true)
            }
        }
    }

}


export default DetailsForm