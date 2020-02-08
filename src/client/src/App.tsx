import React, { Component } from 'react';
import InputField from './components/InputField';

class App extends Component {
  render() {
    return (
      <div>
        <InputField first_name={'Talel'} second_name={'Dayekh'}/>
      </div>
    );
  }
}

export default App;
