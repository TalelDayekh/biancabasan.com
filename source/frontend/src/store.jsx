// Redux
import { createStore, compose, applyMiddleware } from 'redux';
import thunk from 'redux-thunk';
// Local imports
import rootReducer from './reducers';


const store = createStore(
    rootReducer,
    compose(applyMiddleware(thunk),
    window.__REDUX_DEVTOOLS_EXTENSION__ && window.__REDUX_DEVTOOLS_EXTENSION__()
    )
);


export default store;