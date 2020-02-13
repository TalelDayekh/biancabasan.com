import React from 'react';
import styles from './UserInput.module.scss';

interface UserInputProps {
  shortField: boolean;
}

const UserInput = ({ shortField = false }) => {
  return <input className={styles['user-input']} />;
};

export default UserInput;
