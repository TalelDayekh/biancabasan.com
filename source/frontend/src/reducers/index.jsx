// Redux
import { combineReducers } from 'redux';
// Local imports
import Artwork from './ArtworksReducer.jsx';
import Redirect from './NavReducer.jsx';
import Auth from './AuthReducers.jsx';


export default combineReducers({
    Artwork,
    Redirect,
    Auth
})