import React, { Component } from 'react';


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
                                    const title = artworksKey.title
                                    return <li key={ artworksIndex }>{ title }</li>
                                })}
                            </ul>
                            </li>
                        })}
                    </ul>
                }
            </div>
        )
    }
}


export default AdminMain;