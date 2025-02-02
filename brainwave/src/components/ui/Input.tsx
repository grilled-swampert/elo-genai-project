import React from 'react';

const Input = ({ value, onChange, placeholder, className }) => {
  return (
    <input
      value={value}
      onChange={onChange}
      placeholder={placeholder}
      className={`border rounded p-2 ${className}`}
    />
  );
};

export default Input;
