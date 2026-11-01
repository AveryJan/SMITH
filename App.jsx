import React, {useEffect, useState} from 'react';
import Register from './components/Register/Register.jsx';

const api = async (url, options) => {
  const response = await fetch(url, options);
  const result = await response.json();
  if (!response.ok) throw new Error(result.error || `Request failed (${response.status})`);
  return result;
};

function Login({onLogin}) {
  const [form,setForm]=useState({userName:'',password:''});
  const [error,setError]=useState('');
  const login = async e=>{
    e.preventDefault();setError('');
    try {const result=await api('/djangoapp/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(form)});onLogin(result.userName);}
    catch(e){setError(e.message);}
  };
  return <form className="inline-login" onSubmit={login}>
    <label>Username <input placeholder="Username" required value={form.userName} onChange={e=>setForm({...form,userName:e.target.value})}/></label>
    <label>Password <input placeholder="Password" type="password" required value={form.password} onChange={e=>setForm({...form,password:e.target.value})}/></label>
    <button type="submit">Login</button><span role="alert">{error}</span>
  </form>;
}

function ReviewForm({dealer,onSave}) {
  const [form,setForm]=useState({review:'',purchase:false,purchase_date:'',car_make:'',car_model:'',car_year:'2024'});
  const [error,setError]=useState('');
  const send = async e=>{
    e.preventDefault();setError('');
    try {await api('/djangoapp/add_review',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({...form,dealership:dealer.id})});onSave();}
    catch(e){setError(e.message);}
  };
  return <form className="review-form" onSubmit={send}>
    <h3>Post Review — {dealer.full_name}</h3>
    <label>Review <textarea required rows="4" value={form.review} onChange={e=>setForm({...form,review:e.target.value})}/></label>
    <label>Purchased vehicle <input type="checkbox" checked={form.purchase} onChange={e=>setForm({...form,purchase:e.target.checked})}/></label>
    <label>Purchase date <input type="date" value={form.purchase_date} onChange={e=>setForm({...form,purchase_date:e.target.value})}/></label>
    <label>Car make <input placeholder="Make" value={form.car_make} onChange={e=>setForm({...form,car_make:e.target.value})}/></label>
    <label>Car model <input placeholder="Model" value={form.car_model} onChange={e=>setForm({...form,car_model:e.target.value})}/></label>
    <label>Car year <input type="number" min="2015" max="2035" value={form.car_year} onChange={e=>setForm({...form,car_year:e.target.value})}/></label>
    <button type="submit">Post Review</button><p role="alert">{error}</p>
  </form>;
}

function App() {
  const [page,setPage]=useState('dealers');
  const [username,setUsername]=useState('');
  const [state,setState]=useState('');
  const [dealers,setDealers]=useState([]);
  const [selected,setSelected]=useState(null);
  const [reviews,setReviews]=useState([]);
  const [error,setError]=useState('');
  const [refresh,setRefresh]=useState(0);
  useEffect(()=>{
    let active=true;
    api('/djangoapp/get_dealers'+(state?`/${encodeURIComponent(state)}`:'')).then(r=>{if(active)setDealers(r.dealers)}).catch(e=>{if(active)setError(e.message)});
    return ()=>{active=false};
  },[state]);
  useEffect(()=>{
    if(!selected)return;
    api(`/djangoapp/reviews/dealer/${selected.id}`).then(r=>setReviews(r.reviews)).catch(e=>setError(e.message));
  },[selected,refresh]);
  const states=[...new Set(dealers.map(d=>d.state).filter(Boolean))].sort();
  return <><header><h1>Best Cars</h1><nav>
    <button onClick={()=>setPage('dealers')}>Dealers</button>
    <a href="/static/About.html">About Us</a><a href="/static/Contact.html">Contact Us</a>
    {!username&&<button onClick={()=>setPage('register')}>Register</button>}
  </nav><div className="account">{username?<span>Signed in: <strong>{username}</strong> <button onClick={async()=>{await api('/djangoapp/logout');setUsername('')}}>Logout</button></span>:<Login onLogin={setUsername}/>}</div></header>
  <main>{page==='register'?<Register/>:selected&&page==='detail'?<>
    <button onClick={()=>{setPage('dealers');setSelected(null)}}>Back to Dealers</button>
    <h2>{selected.full_name}</h2><p>{selected.address}, {selected.city}, {selected.state} {selected.zip} · ID {selected.id}</p>
    {username&&<button onClick={()=>setPage('review')}>Review Dealer</button>}
    <h3>Reviews</h3><div className="grid">{reviews.length?reviews.map(r=><article className="card" key={r.id}><p>{r.review}</p><strong>{r.name}</strong><p>{r.car_make} {r.car_model} {r.car_year} · Sentiment: {r.sentiment||'N/A'}</p></article>):<p>No reviews yet</p>}</div>
  </>:page==='review'&&selected?<ReviewForm dealer={selected} onSave={()=>{setRefresh(x=>x+1);setPage('detail')}}/>:<>
    <h2>Find a dealership</h2><label>State <select value={state} onChange={e=>setState(e.target.value)}><option value="">All states</option>{states.map(s=><option key={s}>{s}</option>)}</select></label>
    <div className="grid dealer-grid">{dealers.map(d=><article className="card" key={d.id}><h3>{d.full_name}</h3><p>Dealer ID: {d.id}</p><p>{d.address}, {d.city}, {d.state} {d.zip}</p><button onClick={()=>{setSelected(d);setPage('detail')}}>View Reviews</button></article>)}</div>
  </>}
  <p role="alert">{error}</p></main><footer>Best Cars dealership review capstone</footer></>;
}
export default App;
