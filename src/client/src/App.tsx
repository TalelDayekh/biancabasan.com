import React, { Component } from 'react';
import InputField from './components/InputField';

class App extends Component {
  render() {
    return (
      <div>
        <InputField inputType={'title'} required hidePassword />
        <br />
        <InputField inputType={'technique'} required />
        <br />
        <InputField inputType={'description'} required />
        <br />
        <InputField inputType={'measurement'} shortField required />
        <br />
        <InputField inputType={'new-password'} />
      </div>
    );
  }
}

export default App;
