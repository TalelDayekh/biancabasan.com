import React, { Component } from 'react';
import InputField from './components/InputField';

class App extends Component {
  render() {
    return (
      <div>
        <InputField firstName={'Talel'} secondName={'Dayekh'} />
      </div>
    );
  }
}

export default App;
