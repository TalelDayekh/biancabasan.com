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
                    <input onChange={ this.updateTitle } value={ this.state.title }></input>
                    <br />
                    <button>Save</button>
                </form>
            </div>
        )
    }


    updateTitle = (event) => {
        this.setState({
            title: event.target.value
        })
    }


    createTitle = () => {
        axios.post('http://localhost:8000/artwork_titles/', { title: this.state.title });
        this.setState({
            title: "",
        });
        this.props.history.push('/admin_add_details');
    }


}


export default AddTitle;