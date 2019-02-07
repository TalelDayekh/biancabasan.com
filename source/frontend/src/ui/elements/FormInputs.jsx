import styled, { css } from 'styled-components';


const InputError = css`
    /* Input field */
    border: 2px solid #d32f2f;

    /* Input text */
    color: #d32f2f;
`


export const LongInputField = styled.input`
    /* Input field */
    flex: 1;
    min-width: 0;
    height: 28px;
    background: rgba(207, 216, 220, 0.25);
    border: 2px solid #fff59d;
    border-radius: 40px;
    box-sizing: border-box;

    /* Error */
    ${props => props.raiseError ? InputError : null}
`

export const ShortInputField = styled.input`
    /* Input field */
    flex: 1;
    min-width: 0;
    height: 28px;
    background: rgba(207, 216, 220, 0.25);
    border: 2px solid #fff59d;
    border-radius: 40px;
    box-sizing: border-box;

    /* Error */
    ${props => props.raiseError ? InputError : null}
`

export const TextField = styled.textarea`
    /* Input field */
    flex: 1;
    min-width: 0;
    height: 160px;
    background: rgba(207, 216, 220, 0.25);
    border: 2px solid #fff59d;
    border-radius: 15px;
    box-sizing: border-box;

    /* Error */
    ${props => props.raiseError ? InputError : null}
`
// !! Redesign
export const ImageDropZone = styled.div`
    /* Input field */
    width: 500px;
    height: 500px;
    border: 2px dashed;
`