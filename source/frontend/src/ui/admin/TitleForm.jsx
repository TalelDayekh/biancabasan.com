import React, { Component } from 'react'
// Local imports
// Elements
import {
    LongInputField
} from '../elements/'


class TitleForm extends Component {

    // Variable for input field placeholder
    title='title*'

    render = () => {
        return(
            <React.Fragment>
                <form>
                    <div>
                        <LongInputField
                            id='SET_TITLE'
                            size='1'
                            placeholder={ this.title }
                            onFocus={ this.clearPlaceholder }
                            onBlur={ this.inputValidation }

                            onChange={ (e) => {this.props.setArtwork(e)} }
                            raiseError={ this.props.admin.formError ? true : undefined }
                        />
                    </div>
                </form>
            </React.Fragment>
        )
    }


    clearPlaceholder = (e) => {
        e.target.placeholder=''
        this.props.setFormError(false)
    }

    // Raise error if user inputs nothing
    inputValidation = () => {
        const RegEx = /\S.+/
        if (!(this.props.admin.title.match(RegEx))) {
            this.props.setFormError(true)
        }
    }

}


export default TitleForm