import React, { Component } from 'react'
// Local imports
// Elements
import {
    LongInputField,
    NextButton,
    BackButton
} from '../elements/'


class TitleForm extends Component {

    // Variable for input field placeholder
    title='title*'

    render = () => {
        return(
            <React.Fragment>
                <form id='next' onSubmit={ this.errorCheck }>
                    <div>
                        <LongInputField
                            id='SET_TITLE'
                            size='1'
                            placeholder={ this.title }
                            onFocus={ this.clearPlaceholder }
                            onBlur={ this.inputValidation }
                            defaultValue={ this.props.admin.title }
                            onChange={ (e) => {this.props.setArtwork(e.target.id, e.target.value)} }
                            raiseError={ (this.props.admin.inputErrors.indexOf('SET_TITLE') !== -1) ? true : undefined }
                        />
                    </div>
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

    // Raise error if user inputs nothing
    // or begins string with white space.
    inputValidation = (e) => {
        const RegEx=/\S.*/
        
        if (!(e.target.value.match(RegEx))) {
            this.props.setInputErrors(true, e.target.id)
        }
    }

    // Catch if user input is not matching the requirements
    // and add the input field id to the inputErrors array.
    errorCheck = (e) => {
        e.preventDefault()

        try {
            if ((this.props.admin.title.length===0) || 
                (this.props.admin.inputErrors.indexOf('SET_TITLE') !== -1)) {
                    throw new Error('Required input field is either empty or'
                                    + ' have a faulty value')
            }
            this.switchAdminPanel(e)
        } catch(error) {
            this.props.setInputErrors(true, 'SET_TITLE')
        }
    }

    switchAdminPanel = (e) => {
        this.props.switchAdminPanel(e)
    }

}


export default TitleForm