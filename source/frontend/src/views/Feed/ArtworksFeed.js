import React, { Component } from 'react';

import axios from 'axios';


class ArtworksFeed extends Component {

    componentDidMount = () => {

        axios.get('http://localhost:8000/admin_artworks/artworks_list/').then(
            response => {
                response.data.map((artwork_object, artwork_object_index) => {
                    console.log(artwork_object_index);
                    console.log(artwork_object.title);
                    artwork_object.details.map((details_object, details_object_index) => {
                        console.log(details_object.height);
                        console.log(details_object.width);
                        console.log(details_object.description);
                    })
                    artwork_object.images_list.map((image_object, image_object_index) => {
                        console.log(image_object.id);
                    })
                }
                )
            }
        )

    }


    render = () => {
        return (
            <div>
                <p>Artworks Feed</p>
            </div>
        )
    }

    
}


export default ArtworksFeed;