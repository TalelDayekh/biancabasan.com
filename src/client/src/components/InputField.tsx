import React from 'react';

const InputField = (props) => {
  return (
      <div>
          <h1>{props.first_name}</h1>
          <h1>{props.second_name}</h1>
          <h1>Hello Functional Component</h1>
      </div>
  )
};

export default InputField;
