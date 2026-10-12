import React, { useState } from 'react';

export default function Register() {
  const [form, setForm] = useState({ userName: '', firstName: '', lastName: '', email: '', password: '' });
  const [message, setMessage] = useState('');
  function update(event) { setForm(current => ({ ...current, [event.target.name]: event.target.value })); }
  async function submit(event) {
    event.preventDefault();
    setMessage('Submitting registration...');
    try {
      const response = await fetch('/djangoapp/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      });
      if (!response.ok) throw new Error(`Registration failed (${response.status})`);
      setMessage('Registration completed successfully.');
    } catch (error) { setMessage(error.message); }
  }
  return <main><h1>Sign Up</h1><form onSubmit={submit}>
    {[['userName','Username','text'],['firstName','First Name','text'],['lastName','Last Name','text'],['email','Email','email'],['password','Password','password']].map(([name,label,type]) =>
      <div key={name}><label htmlFor={name}>{label}</label><input id={name} name={name} type={type} value={form[name]} onChange={update} required autoComplete={name === 'password' ? 'new-password' : undefined}/></div>)}
    <button type="submit">Register</button><p role="status">{message}</p>
  </form></main>;
}
