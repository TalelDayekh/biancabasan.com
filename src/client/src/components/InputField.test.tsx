import React from 'react';
import { render } from '@testing-library/react';
import InputField from './InputField';

describe('InputField.tsx', () => {
  test('renders component based on input type', () => {
    const title = render(<InputField inputType="title" />);
    const technique = render(<InputField inputType="technique" />);
    const height = render(<InputField inputType="height" />);
    const width = render(<InputField inputType="width" />);
    const depth = render(<InputField inputType="depth" />);

    expect(title.getByPlaceholderText('Title')).toBeTruthy();
    expect(technique.getByPlaceholderText('Technique')).toBeTruthy();
    expect(height.getByPlaceholderText('Height')).toBeTruthy();
    expect(width.getByPlaceholderText('Width')).toBeTruthy();
    expect(depth.getByPlaceholderText('Depth')).toBeTruthy();
  });
});
