import React, { Component } from 'react'
// Local imports
// Layouts
import {
    ContentWrapper
} from '../layouts/'


// Pagination counters
let year = null
let yearsCurrentIteration = 0
let yearsTotalIterations = 0
let artworksCurrentIteration = 0
let artworksTotalIterations = 0


class Content extends Component {

    componentDidMount = () => {
        window.addEventListener('scroll', this.artworksPagination)
        this.yearsPagination()
    }

    componentWillUnmount = () => {
        window.removeEventListener('scroll', this.artworksPagination)
    }

    render = () => {
        return(
            /////
            <React.Fragment>
                <ContentWrapper>
                </ContentWrapper>
            </React.Fragment>
        )
    }


    // Declare total amount of years pagination
    // and add new years to pagination.
    yearsPagination = () => {
        yearsTotalIterations = this.props.artworks.allYears.length -1
        year = this.props.artworks.allYears[yearsCurrentIteration]

        this.props.addYearToPagination(year)
        yearsCurrentIteration += 1

        // Add the first artwork for the current year
        this.artworksPagination()       
    }

    // Declare total amount of artworks pagination for the
    // current year when the user scrolls to the bottom of
    // the page and add new artworks to pagination. If all
    // artworks for a year has been added, call a function
    // to start over the process with a new year.
    artworksPagination = () => {        
        if ((year && (artworksCurrentIteration === 0)) || 
            (year && (window.innerHeight + window.scrollY >= document.body.offsetHeight))) {
            artworksTotalIterations = this.props.artworks.allArtworks[year].length -1

            if (artworksCurrentIteration <= artworksTotalIterations) {
                this.props.addArtworkToPagination(year, artworksCurrentIteration)
                artworksCurrentIteration += 1
            } else if (artworksCurrentIteration > artworksTotalIterations) {
                artworksCurrentIteration = 0
                this.yearsPagination()
            }
        }
    }

}


export default Content