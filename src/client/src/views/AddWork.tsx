import React, { useState } from 'react';
import InputField from '../components/InputField';

interface AddWorkState {
  title: string;
}

const AddWork: React.FC = () => {
  const [state, setState] = useState<AddWorkState>({
    title: '',
  });

  const updateStateFromChild = (value) => {
      setState({...state, title: value})
  }

  return <InputField inputType={'title'} updateStateFromChild={updateStateFromChild} />;
};

export default AddWork;
