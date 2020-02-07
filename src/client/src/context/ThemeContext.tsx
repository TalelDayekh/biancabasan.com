import React, { Component,  createContext } from 'react'

export const ThemeContext = createContext()

class ThemeContextProvider extends Component {
    state = {
        lightTheme: true,
        light: {syntax: '#555', ui: '#ddd', bg: '#eee'},
        dark: {syntax: '#ddd', ui: '#333', bg: '#555'}
    }
    render() {
        return (
            <ThemeContext.Provider value={{...this.state}}>

            </ThemeContext.Provider>
        )
    }
}

export default ThemeContextProvider