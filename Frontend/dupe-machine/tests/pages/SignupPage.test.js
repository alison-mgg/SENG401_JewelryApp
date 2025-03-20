import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import SignUpPage from '../../src/pages/SignUpPage';
import config from '../../src/config';

/**
 * SignupPage.test.js
 *
 * This file contains automated tests for the SignUpPage component.
 * It uses Jest and React Testing Library to ensure that the component
 * behaves as expected. The tests cover the following scenarios:
 * - Rendering the SignUpPage component
 * - Allowing a user to sign up successfully
 * - Displaying an error message when sign-up fails
 *
 * The fetch function is mocked to simulate API responses for testing purposes.
 */

// Mock the fetch function
global.fetch = jest.fn(() =>
  Promise.resolve({
    ok: true,
    json: () => Promise.resolve({}),
  })
);

// Tests for the SignUpPage component
describe('SignUpPage', () => {
  beforeEach(() => {
    fetch.mockClear();
  });

  // Test that the SignUpPage component renders
  test('renders SignUpPage component', () => {
    render(<SignUpPage />);
    expect(screen.getByText('Sign Up')).toBeInTheDocument();
  });

  // Test that the user can sign up
  test('allows user to sign up', async () => {
    render(<SignUpPage />);

    fireEvent.change(screen.getByPlaceholderText('Username'), {
      target: { value: 'testuser' },
    });
    fireEvent.change(screen.getByPlaceholderText('Email'), {
      target: { value: 'testuser@example.com' },
    });
    fireEvent.change(screen.getByPlaceholderText('Password'), {
      target: { value: 'password123' },
    });

    fireEvent.click(screen.getByText('Sign Up'));

    expect(fetch).toHaveBeenCalledWith(`${config.apiURL}/signup`, expect.any(Object));
    expect(await screen.findByText('Signup successful!')).toBeInTheDocument();
  });

  // Test that an error message is displayed when sign-up fails
  test('shows error message on sign-up failure', async () => {
    fetch.mockImplementationOnce(() =>
      Promise.resolve({
        ok: false,
        json: () => Promise.resolve({ message: 'Sign-up error' }),
      })
    );

    render(<SignUpPage />);

    fireEvent.change(screen.getByPlaceholderText('Username'), {
      target: { value: 'testuser' },
    });
    fireEvent.change(screen.getByPlaceholderText('Email'), {
      target: { value: 'testuser@example.com' },
    });
    fireEvent.change(screen.getByPlaceholderText('Password'), {
      target: { value: 'password123' },
    });

    fireEvent.click(screen.getByText('Sign Up'));

    expect(fetch).toHaveBeenCalledWith(`${config.apiURL}/signup`, expect.any(Object));
    expect(await screen.findByText('Sign-up error: Sign-up error')).toBeInTheDocument();
  });
});