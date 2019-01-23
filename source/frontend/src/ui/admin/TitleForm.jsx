import React, { Component } from 'react';
// Redux
import { connect } from 'react-redux';
// Local imports
import '../../App.css';
import {
    setArtwork
} from '../../actions/';
import {
    LongInputField,
    NextButton,
    BackButton
} from '../elements/';


class TitleForm extends Component {

    // Variable for input field placeholder
    title="Title*"

    render = () => {
        return(
            <React.Fragment>
                <form id="next" onSubmit={ this.redirect }>
                    <div className = "top-input-flex-container">
                        <LongInputField
                            id="SET_TITLE"
                            size="1"
                            placeholder={ this.title }
                            // onFocus = ""
                            // onBlur = ""
                            defaultValue={ this.props.retrieveArtwork.title }
                            onChange={ (e) => { this.props.setArtwork(e) } }
                            raiseError=""
                        />
                    </div>
                    <NextButton type="submit">Next</NextButton>
                </form>
                <BackButton>Back</BackButton>
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


export default connect(mapStateToProps, mapDispatchToProps)(TitleForm);