import React from 'react';

type InputFieldProps = {
  firstName: string;
  secondName: string;
};

const InputField: React.FunctionComponent<InputFieldProps> = ({
  firstName,
  secondName,
}) => {
  return (
    <div>
      <h1>{firstName}</h1>
      <h1>{secondName}</h1>
      <h1>Hello Functional Component</h1>
    </div>
  );
};

export default InputField;
