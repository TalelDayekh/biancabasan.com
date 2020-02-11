import React, { useState } from 'react';

const InputField = props => {
  useState({ valid: false });
  const doSomething = () => {
    console.log('Print something...');
  };
  doSomething();
  switch (props.inputType) {
    case 'password':
      return <h1>Password</h1>;
    case 'title':
      return <h1>Title</h1>;
  }
};

export default InputField;
