import React, { Component } from 'react';
import InputField from './components/InputField';

class App extends Component {
  render() {
    return (
      <div>
        <InputField inputType={'title'} required />
        <br />
        <InputField inputType={'measurement'} shortField />
      </div>
    );
  }
}

export default App;
