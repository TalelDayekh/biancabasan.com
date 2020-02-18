import React, { useState } from 'react';
import styles from './InputField.module.scss';

interface InputFieldProps {
  inputType: string;
  required?: boolean;
  shortField?: boolean;
  hidePassword?: boolean;
}

interface InputFieldState {
  userInput: string;
  inputError: string;
}

const InputField: React.FC<InputFieldProps> = ({
  inputType = 'title',
  required = false,
  shortField = false,
  hidePassword = false,
}) => {
  const [state, setState] = useState<InputFieldState>({
    userInput: '',
    inputError: '',
  });

  const validateTextAndNumberInput = () => {
    let inputLength: number =
      inputType === 'title' ? 80 : inputType === 'technique' ? 255 : Infinity;

    if (required && state.userInput.length <= 0) {
      setState({ ...state, inputError: 'Input field cannot be empty' });
    } else if (inputType === 'measurement' && isNaN(Number(state.userInput))) {
      setState({ ...state, inputError: 'Input has to be a number' });
    } else if (state.userInput.length > inputLength) {
      setState({
        ...state,
        inputError: `Input cannot be longer than ${inputLength} characters`,
      });
    }
  };

  const validatePassword = () => {
    console.log('Password validator');
  };

  const selectInputValidator = () => {
    switch (inputType) {
      case 'title':
      case 'technique':
      case 'description':
      case 'measurement':
        validateTextAndNumberInput();
        break;
      case 'new-password':
        validatePassword();
        break;
    }
  };

  if (inputType === 'description') {
    return (
      <textarea
        className={`
          ${styles['user-input-textarea']} 
          ${shortField && styles['short-field']}
          ${state.inputError && styles['error']}
        `}
        onBlur={() => selectInputValidator()}
        onFocus={() => setState({ ...state, inputError: '' })}
        onChange={e => setState({ ...state, userInput: e.target.value })}
      />
    );
  } else {
    return (
      <input
        className={`
          ${styles['user-input']} 
          ${shortField && styles['short-field']}
          ${state.inputError && styles['error']}
        `}
        onBlur={() => selectInputValidator()}
        onFocus={() => setState({ ...state, inputError: '' })}
        onChange={e => setState({ ...state, userInput: e.target.value })}
        type={hidePassword ? 'password' : 'text'}
      />
    );
  }
};

export default InputField;
