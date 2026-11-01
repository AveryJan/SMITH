import React, { useState } from 'react';

const fields = [
  { name: 'userName', label: 'Username', type: 'text', autoComplete: 'username' },
  { name: 'firstName', label: 'First Name', type: 'text', autoComplete: 'given-name' },
  { name: 'lastName', label: 'Last Name', type: 'text', autoComplete: 'family-name' },
  { name: 'email', label: 'Email', type: 'email', autoComplete: 'email' },
  { name: 'password', label: 'Password', type: 'password', autoComplete: 'new-password' }
];

export default function Register() {
  const [form, setForm] = useState({userName:'', firstName:'', lastName:'', email:'', password:''});
  const [status, setStatus] = useState('');
  const [busy, setBusy] = useState(false);
  const change = (e) => setForm(s => ({...s, [e.target.name]: e.target.value}));
  const submit = async (e) => {
    e.preventDefault();
    setBusy(true);
    setStatus('');
    try {
      const res = await fetch('/djangoapp/register', {
        method: 'POST',
        credentials: 'same-origin',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form)
      });
      if (!res.ok) throw new Error(`Registration failed (${res.status}).`);
      setStatus('Registration completed.');
    } catch(err) { setStatus(err.message); }
    finally { setBusy(false); }
  };
  return <main><h1>Sign-up</h1><form onSubmit={submit}>
    {fields.map(({name,label,type,autoComplete}) =>
      <div key={name}>
        <label htmlFor={name}>{label}</label>
        <input id={name} name={name} type={type} placeholder={label} autoComplete={autoComplete}
          value={form[name]} onChange={change} required />
      </div>
    )}
    <button type="submit" disabled={busy}>Register</button>
    <p role="status" aria-live="polite">{status}</p>
  </form></main>;
}
