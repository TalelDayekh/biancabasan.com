import React, { useState } from 'react';
import styles from './InputField.module.scss';

interface InputFieldProps {
  inputType: string;
  required?: boolean;
  shortField?: boolean;
}

interface InputFieldState {
  userInput: string;
  inputError: string;
}

const InputField: React.FC<InputFieldProps> = ({
  inputType = 'title',
  required = false,
  shortField = false,
}) => {
  const [state, setState] = useState<InputFieldState>({
    userInput: '',
    inputError: '',
  });

  const validateTextInput = () => {
    if (required && state.userInput.length <= 0) {
      setState({ ...state, inputError: 'Input field cannot be empty' });
    }
  };

  const selectInputValidator = () => {
    switch (inputType) {
      case 'title':
        validateTextInput();
        break;
      case 'measurement':
        console.log('Use measurement validator');
        break;
    }
  };

  return (
    <input
      className={`
        ${styles['user-input']} 
        ${shortField && styles['short-field']}`}
      onBlur={() => selectInputValidator()}
      onFocus={() => setState({ ...state, inputError: '' })}
      onChange={e => setState({ ...state, userInput: e.target.value })}
    />
  );
};

export default InputField;
