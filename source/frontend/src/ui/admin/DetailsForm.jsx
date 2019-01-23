import React, { Component } from 'react';
// Redux
import { connect } from 'react-redux';
// Local imports
import '../../App.css';
import {
    setArtwork
} from '../../actions/';
import {
    ShortInputField,
    LongInputField,
    TextField,
    NextButton,
    BackButton
} from '../elements/';


class DetailsForm extends Component {

    render = () => {
        return(
            <React.Fragment>
                <form id="next" onSubmit={ this.redirect }>
                    <div className="top-input-flex-container">
                        <ShortInputField
                            id="SET_YEAR_FROM"
                            size="1"
                            placeholer=""
                            // onFocus = {}
                            // onBlur = {}
                            defaultValue=""
                            onChange={ (e) => { this.props.setArtwork(e) } }
                        />
                        <div className="spacer-div-middle"/>
                        <ShortInputField
                            id="SET_YEAR_TO"
                            size="1"
                            placeholer=""
                            // onFocus = {}
                            // onBlur = {}
                            defaultValue=""
                            onChange={ (e) => { this.props.setArtwork(e) } }
                            raiseError=""
                        />
                    </div>
                    <div className="input-flex-container">
                        <LongInputField
                            id="SET_MATERIAL"
                            size="1"
                            placeholder=""
                            // onFocus = {}
                            // onBlur = {}
                            defaultValue=""
                            onChange={ (e) => { this.props.setArtwork(e) } }
                            raiseError=""
                        />
                    </div>
                    <div className="input-flex-container">
                        <ShortInputField
                            id="SET_HEIGHT"
                            size="1"
                            placeholder=""
                            // onFocus = {}
                            // onBlur = {}
                            defaultValue=""
                            onChange={ (e) => { this.props.setArtwork(e) } }
                            raiseError=""
                        />
                        <div className="spacer-div-right"/>
                    </div>
                    <div className="input-flex-container">
                        <ShortInputField
                            id="SET_WIDTH"
                            size="1"
                            placeholder=""
                            // onFocus = {}
                            // onBlur = {}
                            defaultValue=""
                            onChange={ (e) => { this.props.setArtwork(e) } }
                            raiseError=""
                        />
                        <div className="spacer-div-right"/>
                    </div>
                    <div className="input-flex-container">
                        <ShortInputField
                            id="SET_DEPTH"
                            size="1"
                            placeholder=""
                            // onFocus = {}
                            // onBlur = {}
                            defaultValue=""
                            onChange={ (e) => { this.props.setArtwork(e) } }
                        />
                        <div className="spacer-div-right"/>
                    </div>
                    <div className="input-flex-container">
                        <TextField
                            id="SET_DESCRIPTION"
                            size="1"
                            placeholder=""
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


const mapStateToProps = (state) => {
    return {
        retrieveArtwork: state.Artwork
    }
}

const mapDispatchToProps = (dispatch) => {
    return {
        setArtwork: (e) => {
            dispatch(setArtwork(e.target.id, e.target.value))
        }
    }
}


export default connect(mapStateToProps, mapDispatchToProps)(DetailsForm);