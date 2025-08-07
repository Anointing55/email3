import { render, fireEvent } from '@testing-library/react';
import UrlInput from '../components/UrlInput';

describe('UrlInput', () => {
  it('renders correctly', () => {
    const { getByText, getByPlaceholderText } = render(
      <UrlInput onSubmit={() => {}} />
    );
    
    expect(getByText('Enter URLs (one per line)')).toBeInTheDocument();
    expect(getByPlaceholderText('https://example.com')).toBeInTheDocument();
  });
  
  it('submits URLs', () => {
    const mockSubmit = jest.fn();
    const { getByText, getByPlaceholderText } = render(
      <UrlInput onSubmit={mockSubmit} />
    );
    
    const textarea = getByPlaceholderText('https://example.com');
    fireEvent.change(textarea, { target: { value: 'https://example.com\nhttps://test.com' } });
    
    const button = getByText('Extract Contact Information');
    fireEvent.click(button);
    
    expect(mockSubmit).toHaveBeenCalledWith([
      'https://example.com',
      'https://test.com'
    ]);
  });
  
  it('shows error on empty submit', () => {
    const mockSubmit = jest.fn();
    const { getByText } = render(
      <UrlInput onSubmit={mockSubmit} />
    );
    
    const button = getByText('Extract Contact Information');
    fireEvent.click(button);
    
    expect(mockSubmit).not.toHaveBeenCalled();
    expect(getByText('Please enter at least one URL')).toBeInTheDocument();
  });
});
