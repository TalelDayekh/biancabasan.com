import React, { Component } from 'react'


class AdminMain extends Component {

    componentDidMount = () => {
        this.props.loadSortedArtworks()
    }

    render = () => {
        return(
            <React.Fragment>
                <h4>Admin Main</h4>
            </React.Fragment>
        )
    }

}


export default AdminMain