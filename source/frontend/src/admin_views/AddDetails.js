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
                <form>
                    <p>Height</p>
                    <input onChange={ this.updateDetails } name="height"></input>
                    <br />
                    <br />
                    <p>Widht</p>
                    <input onChange={ this.updateDetails } name="width"></input>
                    <br />
                    <br />
                    <p>Description</p>
                    <textarea onChange={ this.updateDetails } name="description" cols="60" rows="15"></textarea>
                    <br />
                    <button>Save</button>
                </form>
            </div>
        )
    }


    updateDetails = (event) => {
        this.setState({
            [event.target.name]: event.target.value
        }) 
    }


}


export default AddDetails;