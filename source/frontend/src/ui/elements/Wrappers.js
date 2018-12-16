import styled, { createGlobalStyle } from 'styled-components';


export const PageColorTheme = createGlobalStyle`
    body {
        background: ${props => (props.metallicXerox ? 'linear-gradient(90deg, pink, aqua)' : '#fff')}
    }
`


export const MainWrapper = styled.div`
    display: grid;
    grid-template-columns: repeat(12, 1fr);
    max-width: 1340px;
    margin: 0 auto;
`