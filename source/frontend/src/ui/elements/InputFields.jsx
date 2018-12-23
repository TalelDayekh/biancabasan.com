import styled from 'styled-components';


export const LongInputField = styled.input`
    flex: 1;
    min-width: 0;
    height: 28px;
    background: rgba(207, 216, 220, 0.25);
    border: 2px solid #FFF59D;
    border-radius: 40px;
    box-sizing: border-box;
    font-family: 'Comfortaa', cursive;
    color: #FFFDE7;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.1em;
    padding-left: 11px;

    ::placeholder {
        color: rgba(255, 253, 231, 0.7);
        opacity: 1; /* Firefox */
        font-size: 11px;
    }
    
    /* Placeholder for IE and Edge */
    :-ms-input-placeholder {
        color: rgba(255, 253, 231, 0.7);
        font-size: 11px;
    }
    ::-ms-input-placeholder {
        color: rgba(255, 253, 231, 0.7);
        font-size: 11px;
    }
`

export const ShortInputField = styled.input`
    flex: 1;
    min-width: 0;
    height: 28px;
    background: rgba(207, 216, 220, 0.25);
    border: 2px solid #FFF59D;
    border-radius: 40px;
    box-sizing: border-box;
    font-family: 'Comfortaa', cursive;
    color: #FFFDE7;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.1em;
    padding-left: 11px;

    ::placeholder {
        color: rgba(255, 253, 231, 0.7);
        opacity: 1; /* Firefox */
        font-size: 11px;
    }

    /* Placeholder for IE and Edge */
    :-ms-input-placeholder {
        color: rgba(255, 253, 231, 0.7);
        font-size: 11px;
    }
    ::-ms-input-placeholder {
        color: rgba(255, 253, 231, 0.7);
        font-size: 11px;
    }
`

export const TextField = styled.textarea`
    flex: 1;
    min-width: 0;
    height: 160px;
    background: rgba(207, 216, 220, 0.25);
    border: 2px solid #FFF59D;
    border-radius: 15px;
    box-sizing: border-box;
    font-family: 'Comfortaa', cursive;
    color: #FFFDE7;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.1em;
    padding: 8px 0px 0px 11px;

    ::placeholder {
        color: rgba(255, 253, 231, 0.7);
        opacity: 1; /* Firefox */
        font-size: 11px;
    }

    /* Placeholder for IE and Edge */
    :-ms-input-placeholder {
        color: rgba(255, 253, 231, 0.7);
        font-size: 11px;
    }
    ::-ms-input-placeholder {
        color: rgba(255, 253, 231, 0.7);
        font-size: 11px;
    }
`