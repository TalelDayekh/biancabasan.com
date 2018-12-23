import React, { Component } from 'react';

import { AdminContentWrapper } from '../layouts/Wrappers';
import { AdminHeading } from '../elements/Headings';
import { LongInputField, ShortInputField, TextField } from '../elements/InputFields';
import { SaveButton, BackButton } from '../elements/Buttons';


const headingStyle = {
    marginTop: '160px'
}

const topInputContainer = {
    display: 'flex',
    marginTop: '55px'
}

const inputContainer = {
    display: 'flex',
    marginTop: '28px'
}

const spacerDivMiddle = {
    flex: '0 0 3.904%'
}

const spacerDivRight = {
    flex: '0 0 51.95%'
}

const saveButtonStyle = {
    float: 'left',
    marginTop: '22px'
}

const backButtonStyle = {
    float: 'left',
    margin: '22px 0px 0px 10px'
}


class AddDetails extends Component {

    render = () => {
        
        return(
            <AdminContentWrapper>
                {/* Heading */}
                <AdminHeading style={ headingStyle }>
                    Add some specs and describe your work a bit
                </AdminHeading>

                <form>
                    {/* Input fields */}
                    <div style={ topInputContainer }>
                        <ShortInputField 
                            size="1"
                            name="Created between YYYY"
                            placeholder="Created between YYYY"
                        />
                        <div style={ spacerDivMiddle } />
                        <ShortInputField 
                            size="1" 
                            name="and YYYY*"
                            placeholder="and YYYY*"
                        />
                    </div>
                    <div style={ inputContainer }>
                        <LongInputField 
                            size="1"
                            name="Material*"
                            placeholder="Material*"
                        />
                    </div>
                    <div style={ inputContainer }>
                        <ShortInputField 
                            size="1"
                            name="Height*"
                            placeholder="Height*"
                        />
                        <div style={ spacerDivRight } />
                    </div>
                    <div style={ inputContainer }>
                        <ShortInputField 
                            size="1"
                            name="Width*"
                            placeholder="Width*"
                        />
                        <div style={ spacerDivRight } />
                    </div>
                    <div style={ inputContainer }>
                        <ShortInputField 
                            size="1"
                            name="Depth*"
                            placeholder="Depth*"
                        />
                        <div style={ spacerDivRight } />
                    </div>
                    <div style={ inputContainer }>
                        <TextField 
                            size="1"
                            name="Description*"
                            placeholder="Description*"
                        />
                    </div>

                    {/* Buttons */}
                    <SaveButton style={ saveButtonStyle }>Save</SaveButton>
                    <BackButton style={ backButtonStyle }>Back</BackButton>
                </form>
            </AdminContentWrapper>
        )
    }

}


export default AddDetails;