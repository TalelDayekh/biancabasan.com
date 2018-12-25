import styled, { css } from 'styled-components';


const InputError = css`
    /* Input field */
    border: 2px solid #D32F2F;

    /* Input text */
    color: #D32F2F;

    /* Placeholder text */
    ::placeholder {
        color: #D32F2F;
        opacity: 1; /* Firefox */
    }
    /* Placeholder for IE and Edge */
    :-ms-input-placeholder {
        color: #D32F2F;
    }
    ::-ms-input-placeholder {
        color: #D32F2F;
    }
`

export const LongInputField = styled.input`
    /* Input field */
    flex: 1;
    min-width: 0;
    height: 28px;
    background: rgba(207, 216, 220, 0.25);
    border: 2px solid #FFF59D;
    border-radius: 40px;
    box-sizing: border-box;

    /* Input text */
    font-family: 'Comfortaa', cursive;
    color: #FFFDE7;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.1em;
    padding-left: 11px;

    /* Placeholder text */
    ::placeholder {
        color: rgba(255, 253, 231, 0.7);
        opacity: 1; /* Firefox */
        font-size: 11px;
    }
    /* Placeholder text for IE and Edge */
    :-ms-input-placeholder {
        color: rgba(255, 253, 231, 0.7);
        font-size: 11px;
    }
    ::-ms-input-placeholder {
        color: rgba(255, 253, 231, 0.7);
        font-size: 11px;
    }

    /* Error */
    ${props => props.raiseError ? InputError : null}
`

export const ShortInputField = styled.input`
    /* Input field */
    flex: 1;
    min-width: 0;
    height: 28px;
    background: rgba(207, 216, 220, 0.25);
    border: 2px solid #FFF59D;
    border-radius: 40px;
    box-sizing: border-box;

    /* Input text */
    font-family: 'Comfortaa', cursive;
    color: #FFFDE7;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.1em;
    padding-left: 11px;

    /* Placeholder text */
    ::placeholder {
        color: rgba(255, 253, 231, 0.7);
        opacity: 1; /* Firefox */
        font-size: 11px;
    }
    /* Placeholder text for IE and Edge */
    :-ms-input-placeholder {
        color: rgba(255, 253, 231, 0.7);
        font-size: 11px;
    }
    ::-ms-input-placeholder {
        color: rgba(255, 253, 231, 0.7);
        font-size: 11px;
    }

    /* Error */
    ${props => props.raiseError ? InputError : null}
`

export const TextField = styled.textarea`
    /* Input field */
    flex: 1;
    min-width: 0;
    height: 160px;
    background: rgba(207, 216, 220, 0.25);
    border: 2px solid #FFF59D;
    border-radius: 15px;
    box-sizing: border-box;

    /* Input text */
    font-family: 'Comfortaa', cursive;
    color: #FFFDE7;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.1em;
    padding: 8px 11px 0px 11px;

    /* Placeholder text */
    ::placeholder {
        color: rgba(255, 253, 231, 0.7);
        opacity: 1; /* Firefox */
        font-size: 11px;
    }
    /* Placeholder text for IE and Edge */
    :-ms-input-placeholder {
        color: rgba(255, 253, 231, 0.7);
        font-size: 11px;
    }
    ::-ms-input-placeholder {
        color: rgba(255, 253, 231, 0.7);
        font-size: 11px;
    }

    /* Error */
    ${props => props.raiseError ? InputError : null}
`