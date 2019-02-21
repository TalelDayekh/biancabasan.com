import React, { Component } from 'react'


let counter = 0


class Content extends Component {

    componentDidMount = () => {
        window.addEventListener('scroll', this.addArtworksToView)
        const allArtworks = this.props.allArtworks

        // Add the latest year and related artworks to pagination
        const artworksYear = Object.keys(allArtworks)[counter]
        const artworksArray = Object.values(allArtworks)[counter]
        this.props.addArtworksToPagination(artworksYear, artworksArray)

        // Add total no. of years to state for keeping
        // count of pagination iterations.
        const yearsCount = Object.keys(allArtworks).length
        this.props.yearsTotal(yearsCount)
    }

    render = () => {
        return(
            
            <div onScroll={this.addArtworksToView}>
            </div>
            
        )
    }


    // Add a new year and related artworks to pagination
    // each time the user scrolls to the bottom of page.
    addArtworksToView = () => {
        const allArtworks = this.props.allArtworks
        const maxIterations = this.props.artworksViewsState.totalIterations

        if (window.innerHeight + window.scrollY >= document.body.offsetHeight) {
            // Start adding from the object's second value
            if (counter === 0) {
                counter += 1
            }
            if (counter <= maxIterations) {
                const artworksYear = Object.keys(allArtworks)[counter]
                const artworksArray = Object.values(allArtworks)[counter]
                this.props.addArtworksToPagination(artworksYear, artworksArray)
                counter += 1
            }
        }
    }

}


export default Content