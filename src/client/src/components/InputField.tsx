import React from 'react';
import styles from './InputField.module.scss';

interface InputFieldProps {
  inputType: string;
  required: boolean;
  shortField: boolean;
}

const InputField = ({
  inputType = 'title',
  required = false,
  shortField = false,
}) => {
  const validateTextInput = () => {
    if (required) {
      console.log('Setting to short error state');
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
    />
  );
};

export default InputField;
