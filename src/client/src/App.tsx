import React, { Component } from 'react';
import InputField from './components/InputField';

class App extends Component {
  render() {
    return (
      <div>
        <InputField inputType={'title'} />
        <InputField inputType={'password'} />
      </div>
    );
  }
}

export default App;
