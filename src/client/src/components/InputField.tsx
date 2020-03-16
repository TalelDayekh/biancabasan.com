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
  const { t } = useTranslation();
  const [state, setState] = useState<InputFieldState>({
    inputError: '',
  });
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

  const validateTextAndNumberInput = (
    e:
      | React.FocusEvent<HTMLInputElement>
      | React.FocusEvent<HTMLTextAreaElement>,
  ): void => {
    let inputLength: number =
      inputType === 'title' ? 80 : inputType === 'technique' ? 255 : Infinity;

    if (required && e.target.value.length <= 0) {
      setState({
        ...state,
        inputError: t('errors.user-errors.input-field.0', {
          inputType: placeholderText,
        }),
      });
    } else if (
      (inputType === 'height' ||
        inputType === 'width' ||
        inputType === 'depth') &&
      isNaN(Number(e.target.value))
    ) {
      updateFormState(inputType, '');
      setState({
        ...state,
        inputError: t('errors.user-errors.input-field.1', {
          inputType: placeholderText,
        }),
      });
    } else if (e.target.value.length > inputLength) {
      updateFormState(inputType, '');
      setState({
        ...state,
        inputError: t('errors.user-errors.input-field.2', {
          inputType: placeholderText,
          inputLength: inputLength,
        }),
      });
    }
  };

  const validatePassword = () => {};

  const selectInputValidator = (
    e:
      | React.FocusEvent<HTMLInputElement>
      | React.FocusEvent<HTMLTextAreaElement>,
  ): void => {
    switch (inputType) {
      case 'title':
      case 'technique':
      case 'height':
      case 'width':
      case 'depth':
      case 'description':
        validateTextAndNumberInput(e);
        break;
      case 'password':
        validatePassword();
        break;
    }
  };

  if (inputType === 'description') {
    return (
      <>
        <textarea
          className={`
            ${styles['user-input-textarea']}
            ${shortField && styles['short-field']}
            ${state.inputError && styles['error']}
          `}
          placeholder={placeholderText}
          onFocus={e => {
            placeholder(e);
            setState({ ...state, inputError: '' });
          }}
          onBlur={e => {
            placeholder(e);
            selectInputValidator(e);
          }}
          onChange={e => updateFormState(inputType, e.target.value)}
        />
        <h1>{state.inputError}</h1>
      </>
    );
  } else {
    return (
      <>
        <input
          className={`
            ${styles['user-input']}
            ${shortField && styles['short-field']}
            ${state.inputError && styles['error']}
          `}
          placeholder={placeholderText}
          onFocus={e => {
            placeholder(e);
            setState({ ...state, inputError: '' });
          }}
          onBlur={e => {
            placeholder(e);
            selectInputValidator(e);
          }}
          onChange={e => updateFormState(inputType, e.target.value)}
          type={hidePassword ? 'password' : 'text'}
        />
        <h1>{state.inputError}</h1>
      </>
    );
  }
};

export default InputField;
