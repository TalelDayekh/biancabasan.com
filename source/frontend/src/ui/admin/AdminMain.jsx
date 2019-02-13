import React, { Component } from 'react';
// React Router
import {
    Link
} from 'react-router-dom';


class AdminMain extends Component {

    componentDidMount = () => {
        this.props.loadArtworks();
    }
    render = () => {
        return(
            <div>
                {
                    (this.props.retrieveArtworks.requestLoaded === false) ?
                    <h2>Spinner...</h2>
                    :
                    <ul>
                        {Object.keys(this.props.retrieveArtworks.artworksList).map((yearsKey, yearsIndex) => {
                            const years = yearsKey
                            return <li key={ yearsIndex }>{ years }
                            <ul>
                                {this.props.retrieveArtworks.artworksList[years].map((artworksKey, artworksIndex) => {
                                    const artworkTitle = artworksKey.title
                                    const artworkId = artworksKey.id
                                    return <li key={ artworksIndex }>
                                        <Link 
                                            to="/admin/admin_title/"
                                            onClick={ () => { this.editMode(artworkId) } }
                                        >{ artworkTitle }</Link>
                                    </li>
                                })}
                            </ul>
                            </li>
                        })}
                    </ul>
                }
            </div>
        )
    }


    editMode = (artworkId) => {
        this.props.toggleEditMode(true, artworkId);
    }
}


export default AdminMain;