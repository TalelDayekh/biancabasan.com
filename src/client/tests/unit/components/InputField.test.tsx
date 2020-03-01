import React from 'react';
import { render } from '@testing-library/react';
import InputField from '../../../src/components/InputField';

describe('InputField.tsx', () => {
  test('renders component based on input type', () => {
    const titleInput = render(<InputField inputType="title" />);
    const techniqueInput = render(<InputField inputType="technique" />);
    const heightInput = render(<InputField inputType="height" />);
    const widthInput = render(<InputField inputType="width" />);
    const depthInput = render(<InputField inputType="depth" />);
    const descriptionInput = render(<InputField inputType="description" />);

    expect(titleInput.getByPlaceholderText('Title')).toBeTruthy();
    expect(techniqueInput.getByPlaceholderText('Technique')).toBeTruthy();
    expect(heightInput.getByPlaceholderText('Height')).toBeTruthy();
    expect(widthInput.getByPlaceholderText('Width')).toBeTruthy();
    expect(depthInput.getByPlaceholderText('Depth')).toBeTruthy();
    expect(descriptionInput.getByPlaceholderText('Description')).toBeTruthy();
  });
});
