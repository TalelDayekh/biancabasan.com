import React, { useState } from 'react';
import InputField from '../components/InputField';

interface AddWorkState {
  title: string;
  technique: string;
  height: number;
  width: number;
  depth: number;
  description: string;
}

const AddWork: React.FC = () => {
  const [state, setState] = useState<AddWorkState>({
    title: '',
    technique: '',
    height: undefined,
    width: undefined,
    depth: undefined,
    description: '',
  });

  const updateFormState = (key: string, value: string | number): void => {
    setState({ ...state, [key]: value });
  };

  return (
    <InputField
      inputType={'title'}
      updateFormState={updateFormState}
      required
    />
  );
};

export default AddWork;
