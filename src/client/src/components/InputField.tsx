import React, { useState } from 'react';
import styles from './InputField.module.scss';

const InputField = props => {
  useState({ valid: false });
  return <input className={styles.inputfield} />;
};

export default InputField;
