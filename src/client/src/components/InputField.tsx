import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import styles from './InputField.module.scss';

interface InputFieldProps {
  inputType: string;
  required?: boolean;
  shortField?: boolean;
  hidePassword?: boolean;
  updateFormState: Function;
}

interface InputFieldState {
  inputError: string;
}

const InputField: React.FC<InputFieldProps> = ({
  inputType = 'title',
  required = false,
  shortField = false,
  hidePassword = false,
  updateFormState,
}) => {
  let placeholderText: string =
    inputType.charAt(0).toUpperCase() + inputType.slice(1);

  const [state, setState] = useState<InputFieldState>({
    inputError: '',
  });

  const placeholder = (
    e:
      | React.FocusEvent<HTMLInputElement>
      | React.FocusEvent<HTMLTextAreaElement>,
  ): void => {
    e.type === 'focus'
      ? (e.target.placeholder = '')
      : (e.target.placeholder = placeholderText);
  };

  const validateTextAndNumberInput = (): void => {
    let inputLength: number =
      inputType === 'title' ? 80 : inputType === 'technique' ? 255 : Infinity;
  };

  if (inputType === 'description') {
    return (
      <>
        <textarea
          placeholder={placeholderText}
          onFocus={placeholder}
          onBlur={placeholder}
        />
      </>
    );
  } else {
    return (
      <>
        <input
          placeholder={placeholderText}
          onFocus={placeholder}
          onBlur={placeholder}
          onChange={e => updateFormState(inputType, e.target.value)}
        />
      </>
    );
  }
};

export default InputField;
