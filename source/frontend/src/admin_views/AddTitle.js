import React, { Component } from 'react';

import axios from 'axios';


class AddTitle extends Component {
    state = {
        title: "",
    }


    render() {
        return(
            <div>
                <form onSubmit={ this.createTitle }>
                    <p>Title</p>
                    <input onChange={ this.updateTitle } value={ this.state.title }/>
                    <br />
                    <button type="submit">Save</button>
                </form>
            </div>
        )
    }


    updateTitle = (event) => {
        this.setState({
            title: event.target.value
        })
    }


    createTitle = (event) => {
        axios.post('http://localhost:8000/artwork_titles/', { title: this.state.title })
        .then(response => {
            this.props.history.push({
                pathname: '/admin_add_details/',
                state: { artwork_object_id: response.data.id }
            })
        });
        this.setState({
            title: "",
        });
        event.preventDefault();
    }


}


export default AddTitle;