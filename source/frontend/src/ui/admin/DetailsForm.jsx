import React, { Component } from 'react';
// Local imports
import '../../App.css';
import {
    ShortInputField,
    LongInputField,
    TextField,
    NextButton,
    BackButton
} from '../elements/';


class DetailsForm extends Component {

    // Variables for input field placeholders
    yearFrom="Created between YYYY*"
    yearTo="and YYYY*"
    material="Materials*"
    height="Height*"
    width="Width*"
    depth="Depth"
    description="Description*"

    render = () => {
        return(
            <React.Fragment>
                <form id="next" onSubmit={ this.redirect }>
                    <div className="top-input-flex-container">
                        <ShortInputField
                            id="SET_YEAR_FROM"
                            size="1"
                            placeholder={ this.yearFrom }
                            // onFocus = {}
                            // onBlur = {}
                            defaultValue={ this.props.retrieveArtwork.yearFrom }
                            onChange={ (e) => { this.props.setArtwork(e) } }
                        />
                        <div className="spacer-div-middle"/>
                        <ShortInputField
                            id="SET_YEAR_TO"
                            size="1"
                            placeholder={ this.yearTo }
                            // onFocus = {}
                            // onBlur = {}
                            defaultValue={ this.props.retrieveArtwork.yearTo }
                            onChange={ (e) => { this.props.setArtwork(e) } }
                            raiseError=""
                        />
                    </div>
                    <div className="input-flex-container">
                        <LongInputField
                            id="SET_MATERIAL"
                            size="1"
                            placeholder={ this.material }
                            // onFocus = {}
                            // onBlur = {}
                            defaultValue={ this.props.retrieveArtwork.material }
                            onChange={ (e) => { this.props.setArtwork(e) } }
                            raiseError=""
                        />
                    </div>
                    <div className="input-flex-container">
                        <ShortInputField
                            id="SET_HEIGHT"
                            size="1"
                            placeholder={ this.height }
                            // onFocus = {}
                            // onBlur = {}
                            defaultValue={ this.props.retrieveArtwork.height }
                            onChange={ (e) => { this.props.setArtwork(e) } }
                            raiseError=""
                        />
                        <div className="spacer-div-right"/>
                    </div>
                    <div className="input-flex-container">
                        <ShortInputField
                            id="SET_WIDTH"
                            size="1"
                            placeholder={ this.width }
                            // onFocus = {}
                            // onBlur = {}
                            defaultValue={ this.props.retrieveArtwork.width }
                            onChange={ (e) => { this.props.setArtwork(e) } }
                            raiseError=""
                        />
                        <div className="spacer-div-right"/>
                    </div>
                    <div className="input-flex-container">
                        <ShortInputField
                            id="SET_DEPTH"
                            size="1"
                            placeholder={ this.depth }
                            // onFocus = {}
                            // onBlur = {}
                            defaultValue={ this.props.retrieveArtwork.depth }
                            onChange={ (e) => { this.props.setArtwork(e) } }
                        />
                        <div className="spacer-div-right"/>
                    </div>
                    <div className="input-flex-container">
                        <TextField
                            id="SET_DESCRIPTION"
                            size="1"
                            placeholder={ this.description }
                            // onFocus = {}
                            // onBlur = {}
                            defaultValue={ this.props.retrieveArtwork.description }
                            onChange={ (e) => { this.props.setArtwork(e) } }
                            raiseError=""
                        />
                    </div>
                    <NextButton type="submit">Next</NextButton>
                </form>
                <BackButton id="back" onClick={ this.redirect }>Back</BackButton>
            </React.Fragment>   
        )
    }


    redirect = (e) => {
        this.props.redirect(e);
        e.preventDefault();
    }

    // Form validation
}


export default DetailsForm;