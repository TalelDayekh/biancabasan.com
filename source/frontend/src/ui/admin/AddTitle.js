import React, { Component } from 'react';

import {
    Link
} from 'react-router-dom';

import { AdminContentWrapper } from '../layouts/Wrappers';
import { AdminHeading } from '../elements/Headings'
import { LongInputField } from '../elements/InputFields';
import { SaveButton, BackButton } from '../elements/Buttons';


const headingStyle = {
    marginTop: '230px',
}

const titleInputStyle = {
    marginTop: '55px',
}

const saveButtonStyle = {
    float: 'left',
    marginTop: '22px',
}

const backButtonStyle = {
    float: 'left',
    marginTop: '22px',
    marginLeft: '10px',
}


class AddTitle extends Component {

    render = () => {
        return(
            <AdminContentWrapper>
                {/* Heading */}
                <div>
                    <AdminHeading style={ headingStyle }>
                        Did you make a new piece? Cool! What's it called?
                    </AdminHeading>
                </div>

                {/* Input field */}
                <LongInputField style={ titleInputStyle } />

                {/* Buttons */}
                <Link to="/admin/add_details/">
                    <SaveButton style={ saveButtonStyle }>Save</SaveButton>
                </Link>
                <Link to="/admin/">
                    <BackButton style={ backButtonStyle }>Back</BackButton>
                </Link>
            </AdminContentWrapper>
        )
    }

}


export default AddTitle;