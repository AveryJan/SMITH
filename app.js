/** Best Cars dealership API: standalone Node.js, no external runtime modules. */
'use strict';
const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const dataDir = path.join(__dirname, 'data');
const dealersPath = path.join(dataDir, 'dealerships.json');
const reviewsPath = path.join(dataDir, 'reviews.json');
const port = Number(process.env.DEALER_PORT || 3030);
const readList = (filename, field) => {
  const parsed = JSON.parse(fs.readFileSync(filename, 'utf8'));
  if (!Array.isArray(parsed[field])) throw new Error('Invalid '+field+' fixture');
  return parsed[field];
};
const send = (res, code, value) => {
  res.writeHead(code, {'Content-Type':'application/json; charset=utf-8', 'Access-Control-Allow-Origin':'*', 'Access-Control-Allow-Headers':'Content-Type', 'Access-Control-Allow-Methods':'GET,POST,OPTIONS', 'Cache-Control':'no-store'});
  res.end(JSON.stringify(value));
};
function handler(req,res) {
  const route = new URL(req.url, 'http://localhost').pathname;
  if(req.method==='OPTIONS') return send(res,204,{});
  if(req.method==='GET') {
    let dealers, reviews;
    try { dealers=readList(dealersPath,'dealerships'); reviews=readList(reviewsPath,'reviews'); }
    catch(e) { return send(res,503,{error:'Data files unavailable: '+e.message}); }
    if(route==='/') return send(res,200,{message:'Best Cars dealership API'});
    if(route==='/health') return send(res,200,{status:'ok',dealers:dealers.length,reviews:reviews.length});
    if(route==='/fetchDealers') return send(res,200,dealers);
    let match=route.match(/^\/fetchDealers\/([^/]+)$/);
    if(match) return send(res,200,dealers.filter(d=>String(d.state).toLowerCase()===decodeURIComponent(match[1]).toLowerCase()));
    match=route.match(/^\/fetchDealer\/(\d+)$/);
    if(match) return send(res,200,dealers.filter(d=>Number(d.id)===Number(match[1])));
    if(route==='/fetchReviews') return send(res,200,reviews);
    match=route.match(/^\/fetchReviews\/dealer\/(\d+)$/);
    if(match) return send(res,200,reviews.filter(d=>Number(d.dealership)===Number(match[1])));
  }
  if(req.method==='POST'&&route==='/insert_review') {
    let input='';
    req.on('data',part=>{ input+=part; if(input.length>1024*64) req.destroy(); });
    req.on('end',()=>{
      let body;
      try { body=JSON.parse(input); } catch(e){return send(res,400,{error:'Invalid JSON'});}
      if(!body||typeof body.review!=='string'||!body.review.trim()||!Number.isInteger(Number(body.dealership))||Number(body.dealership)<1)
        return send(res,400,{error:'Review text and a valid dealership ID required'});
      const reviews=readList(reviewsPath,'reviews');
      const newReview = {id: Math.max(0,...reviews.map(r=>Number(r.id)||0))+1,
        name:String(body.name||'Guest').slice(0,100),dealership:Number(body.dealership),
        review:body.review.trim().slice(0,2500),purchase:Boolean(body.purchase),
        purchase_date:String(body.purchase_date||''),car_make:String(body.car_make||''),
        car_model:String(body.car_model||''),car_year:Number(body.car_year)||null};
      const positive=/\b(great|fantastic|excellent|love|helpful|friendly|amazing|good)\b/i.test(newReview.review);
      const negative=/\b(terrible|bad|awful|poor|worst|horrible)\b/i.test(newReview.review);
      newReview.sentiment= positive&&!negative?'positive':negative&&!positive?'negative':'neutral';
      reviews.push(newReview);
      try {
        fs.writeFileSync(reviewsPath+'.tmp',JSON.stringify({reviews},null,2));
        fs.renameSync(reviewsPath+'.tmp',reviewsPath);
      } catch(e) { return send(res,500,{error:'Unable to save review'}); }
      return send(res,201,newReview);
    });
    return;
  }
  send(res,404,{error:'Not found'});
}
if(require.main===module) http.createServer(handler).listen(port,'0.0.0.0',()=>console.log('Dealer API listening on '+port));
module.exports={handler};
