import React from 'react';
import { useTranslation } from 'react-i18next';
import styles from './InputField.module.scss';

interface InputFieldProps {
  inputType: string;
  required?: boolean;
  shortField?: boolean;
  hidePassword?: boolean;
}

const InputField: React.FC<InputFieldProps> = ({
  inputType = 'title',
  required = false,
  shortField = false,
  hidePassword = false,
}) => {
  let placeholderText: string =
    inputType.charAt(0).toUpperCase() + inputType.slice(1);

  const placeholder = (
    e:
      | React.FocusEvent<HTMLInputElement>
      | React.FocusEvent<HTMLTextAreaElement>,
  ): void => {
    e.type === 'focus'
      ? (e.target.placeholder = '')
      : (e.target.placeholder = placeholderText);
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
        />
      </>
    );
  }
};

export default InputField;
