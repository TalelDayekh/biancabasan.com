// Redux
import { combineReducers } from 'redux';
// Local imports
import Artwork from './ArtworksReducers.jsx';
import Redirect from './NavReducer.jsx';
import Auth from './AuthReducers.jsx';


export default combineReducers({
    Artwork,
    Redirect,
    Auth
})