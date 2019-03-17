import React, { Component } from 'react'
// Local imports
// Layouts
import {
    ContentWrapper
} from '../layouts/'
// Views
import NoContent from './NoContent'


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
            <React.Fragment>
                { (Object.entries(this.props.artworks.allArtworks).length === 0) ?
                    <NoContent/>
                :
                    <React.Fragment>
                        { this.props.artworks.yearsPagination.map((year) => {
                            return (<ContentWrapper>
                                {year}
                                <br/>
                                { this.props.artworks.artworksPagination[year].map((theArtwork) => {
                                    return <div style={{width: '100%', height: '300px', backgroundColor: 'green', borderTop: 'solid 3px yellow'}}>{theArtwork.title}</div>
                                })}
                            </ContentWrapper>)
                        })}
                    </React.Fragment>
                }
            </React.Fragment>
        )
    }


    // Declare total amount of years pagination
    // and add new years to pagination.
    yearsPagination = () => {
        yearsTotalIterations = this.props.artworks.allYears.length -1
        year = this.props.artworks.allYears[yearsCurrentIteration]

        // Add the first artwork for the current year
        this.artworksPagination()

        this.props.addYearToPagination(year)
        yearsCurrentIteration += 1
    }

    // Declare total amount of artworks pagination for the
    // current year when the user scrolls to the bottom of
    // the page and add new artworks to pagination. If all
    // artworks for a year has been added, call a function
    // to start over the process with a new year.
    artworksPagination = () => {
        // Perform pagination on the very first iteration count if a year is stored
        // in the year variable or if a year is stored in the year variable and the
        // user scrolls to the bottom of the page. Do not perform pagination if the
        // allArtworks object has no entries.
        if (((year && (artworksCurrentIteration === 0)) || 
            (year && (window.innerHeight + window.scrollY >= document.body.offsetHeight))) &&
            (Object.entries(this.props.artworks.allArtworks).length > 0)) {

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