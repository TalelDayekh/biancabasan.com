import React, { Component } from 'react'
// React Router
import {
    Link
} from 'react-router-dom'


class AdminMain extends Component {

    componentDidMount = () => {
        this.props.loadSortedArtworks()
        this.props.resetRedirect()
        this.props.toggleEditMode(false)
    }

    render = () => {
        return(
            <React.Fragment>
                { this.props.admin.artworksSorting ?
                    <h2>Spinner...</h2>
                :
                    <ul>
                        { this.props.artworks.allYears.map((year, i) => {
                            return(
                                <li key={i}>
                                    { year }
                                    <ul>
                                        { this.props.admin.allArtworksSorted[year].map((artwork, i) => {
                                            const artworkId = artwork.id
                                            return(
                                                <li key={i}>
                                                    <Link
                                                        to='/admin/title/'
                                                        onClick={ () => {this.editArtwork(artworkId)} }
                                                    >{ artwork.title }</Link>
                                                </li>
                                            )
                                        })}
                                    </ul>
                                </li>
                            )
                        })}
                    </ul> }
            </React.Fragment>
        )
    }


    editArtwork = (artworkId) => {
        this.props.toggleEditMode(true, artworkId)
        this.props.loadArtworkForEdit()
    }

}


export default AdminMain