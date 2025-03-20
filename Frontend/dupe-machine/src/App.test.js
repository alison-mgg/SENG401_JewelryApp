import { render, screen } from '@testing-library/react';
import App from './App';

test('renders login page', () => {
  render(<App />);
  const loginTitleElement = screen.getByRole('heading', { name: /login/i });
  expect(loginTitleElement).toBeInTheDocument();
});
