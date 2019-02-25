import React, { Component } from 'react'
// Redux
import { connect } from 'react-redux'
// Local imports
// Layouts
import {
    GridWrapper,
    HomeWrapper
} from '../layouts/'
// Actions
import {
    addYearToPagination,
    addArtworkToPagination
} from '../../actions/'
// Views
import Content from './Content.jsx'


class Home extends Component {

    render = () => {
        return(
            <React.Fragment>
                <GridWrapper>
                    <HomeWrapper>
                        Home Page
                    </HomeWrapper>
                </GridWrapper>
                { this.props.artworks.artworksLoaded === false ?
                <h2>Spinner...</h2>
                :
                <Content { ...this.props }/>
                }
            </React.Fragment>
        )
    }

}


const mapDispatchToProps = (dispatch) => {
    return {
        // Artwork input data
        addYearToPagination: (year) => { dispatch(addYearToPagination(year)) },
        addArtworkToPagination: (year, artworksCurrentIteration) => { dispatch(addArtworkToPagination(year, artworksCurrentIteration)) }
    }
}


export default connect(null, mapDispatchToProps)(Home)