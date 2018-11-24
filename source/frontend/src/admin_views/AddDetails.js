import React, { Component } from 'react';

import axios from 'axios';


class AddDetails extends Component {
    state = {
        height: "",
        width: "",
        description: "",
    }


    render() {
        return (
            <div>
                <form onSubmit={ this.createDetails }>
                    <p>Height</p>
                    <input onChange={ this.updateDetails } value={ this.state.height } name="height"></input>
                    <br />
                    <br />
                    <p>Widht</p>
                    <input onChange={ this.updateDetails } value={ this.state.width } name="width"></input>
                    <br />
                    <br />
                    <p>Description</p>
                    <textarea onChange={ this.updateDetails } value={ this.state.description } name="description" cols="60" rows="15"></textarea>
                    <br />
                    <button type="submit">Save</button>
                </form>
            </div>
        )
    }


    updateDetails = (event) => {
        this.setState({
            [event.target.name]: event.target.value
        }) 
    }

    
    createDetails = (event) => {
        axios.post('http://localhost:8000/artworks_details/', {
            title_id: this.props.location.state.artwork_id,
            height: this.state.height,
            width: this.state.width,
            description: this.state.description,
        }).then(response => {console.log(response)});
        this.setState({
            height: "",
            width: "",
            description: "",
        });
        event.preventDefault();
    }


}


export default AddDetails;