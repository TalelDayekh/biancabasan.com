import React, { Component } from 'react';
import InputField from './components/InputField';

class App extends Component {
  render() {
    return (
      <div>
        <InputField inputType={'title'} required />
        <br />
        <InputField inputType={'technique'} required />
        <br />
        <InputField inputType={'description'} required />
        <br />
        <InputField inputType={'height'} shortField required />
        <br />
        <InputField inputType={'width'} shortField required />
        <br />
        <InputField inputType={'depth'} shortField required />
        <br />
        <InputField inputType={'password'} />
      </div>
    );
  }
}

export default App;
