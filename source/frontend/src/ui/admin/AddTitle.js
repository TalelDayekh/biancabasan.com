import React, { Component } from 'react';

import styled from 'styled-components';

import { PageDefaults } from '../elements/Wrappers';
import { AdminHeading } from '../elements/Headings';
import { LongInputField } from '../elements/InputFields';
import { SaveButton, BackButton } from '../elements/Buttons';


const ContentWrapper = styled.div`
    grid-column: 5/9;

    /*background: pink; /* REMOVE */
`

const headingStyle = {
    marginTop: '230px',
}

const titleInputStyle = {
    marginTop: '55px',
}


class AddTitle extends Component {

    render = () => {
        return(
            <ContentWrapper>
            <PageDefaults />
                <AdminHeading style={ headingStyle }>
                    Did you make a new piece? Cool! What's it called?
                </AdminHeading>
                <LongInputField style={ titleInputStyle } />
                <br />
                <SaveButton>Save</SaveButton>
                <BackButton>Back</BackButton>
            </ContentWrapper>
        )
    }

}


export default AddTitle;