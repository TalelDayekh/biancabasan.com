// Styling
import styled from 'styled-components';


export const MainWrapper = styled.div`
    display: grid;
    grid-template-columns: repeat(12, 1fr);
    grid-column-gap: 30px;
    max-width: 1340px;
    margin: 0 auto;
`

export const AdminContentWrapper = styled.div`
    grid-column: 5/9;
`