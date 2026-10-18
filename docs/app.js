'use strict';
// Beyond the Signs — shared script: mobile menu, experiment filter, and the SVG charts on results.html.
// Chart data mirror research outputs (matched_backoff_results.json, hierarchy_bootstrap_results.json,
// substitution_attack/results.json); values are copied here so the page works without fetch().

(function(){
  const menu=document.getElementById('menu'),nav=document.getElementById('navigation');
  if(menu&&nav)menu.addEventListener('click',()=>{const o=nav.classList.toggle('open');menu.setAttribute('aria-expanded',String(o));});

  // experiment register filter (methods.html)
  const filters=document.querySelectorAll('[data-filter]');
  filters.forEach(b=>b.addEventListener('click',()=>{
    filters.forEach(x=>{x.classList.toggle('selected',x===b);x.setAttribute('aria-pressed',String(x===b));});
    document.querySelectorAll('#register .experiment').forEach(e=>{e.hidden=b.dataset.filter!=='all'&&e.dataset.kind!==b.dataset.filter;});
  }));
})();

const NS='http://www.w3.org/2000/svg';
// language: pages under docs/it/ set <html lang="it">; T() picks the string, num() the decimal separator
const IT=document.documentElement.lang==='it';
const T=(en,it)=>IT?it:en;
const num=x=>IT?String(x).replace('.',','):String(x);
const LOCALE=IT?'it-IT':'en-GB';
const css=n=>getComputedStyle(document.documentElement).getPropertyValue(n).trim();
function el(tag,attrs,parent,text){
  const e=document.createElementNS(NS,tag);
  for(const k in attrs)e.setAttribute(k,attrs[k]);
  if(text!=null)e.textContent=text;
  if(parent)parent.appendChild(e);
  return e;
}
function svgRoot(host,w,h){host.innerHTML='';return el('svg',{viewBox:`0 0 ${w} ${h}`,preserveAspectRatio:'xMidYMid meet'},host);}
const hostW=host=>Math.max(300,Math.min(900,Math.round(host.clientWidth||760)));

// shared tooltip
const tip=document.createElement('div');tip.className='tip';tip.setAttribute('role','status');
document.addEventListener('DOMContentLoaded',()=>document.body.appendChild(tip));
function showTip(evt,html){tip.innerHTML=html;tip.classList.add('on');moveTip(evt);}
function moveTip(evt){const x=Math.min(evt.clientX+14,innerWidth-262);tip.style.left=x+'px';tip.style.top=(evt.clientY+14)+'px';}
function hideTip(){tip.classList.remove('on');}
function hover(node,html){
  node.style.cursor='default';
  node.addEventListener('mouseenter',e=>showTip(e,html));
  node.addEventListener('mousemove',moveTip);
  node.addEventListener('mouseleave',hideTip);
  node.setAttribute('tabindex','0');
  node.addEventListener('focus',()=>{const r=node.getBoundingClientRect();showTip({clientX:r.right,clientY:r.top},html);});
  node.addEventListener('blur',hideTip);
}
const fmt=(v,d=4)=>num(v.toFixed(d));

/* ---------- data ---------- */
const CORPORA=[
  {id:'voy',label:'Voynich · EVA',fam:'--voynich',dash:'',gains:[0.00123,0.000338,0.001352],
   curve:[4.0362,2.2086,1.9998,1.9988,1.9948,1.9948]},
  {id:'voyc',label:T('Voynich · connected units','Voynich · unità connesse'),fam:'--voynich',dash:'6 4',gains:[0.003702,0.014594,0.003449],
   curve:[3.9311,2.1803,2.0143,2.0071,2.0067,2.0029]},
  {id:'ser',label:'Seraphinianus · OCR',fam:'--seraph',dash:'',gains:[0.098463,0.105175,0.087796],
   curve:[3.6729,2.2125,2.0392,1.9420,1.9274,1.9180]},
  {id:'lat',label:T('Latin · Celsus','Latino · Celso'),fam:'--control',dash:'',gains:[0.350753,0.31892,0.384435],
   curve:[4.0355,3.3234,2.8926,2.5413,2.2450,2.2493]},
  {id:'ita',label:T('Italian · Murri','Italiano · Murri'),fam:'--control',dash:'6 4',gains:[0.295531,0.342462,0.319759],
   curve:[3.9825,3.2097,2.8722,2.5530,2.2949,2.2948]}
];

/* ---------- chart 1a: gain dot-range ---------- */
function gainChart(host){
  const W=hostW(host),narrow=W<560,rowH=narrow?62:50,top=narrow?24:18,left=narrow?14:210,right=narrow?16:40,bottom=40,H=top+rowH*CORPORA.length+bottom;
  const s=svgRoot(host,W,H),ink=css('--ink'),muted=css('--muted'),line=css('--line');
  const xMax=0.4,x=v=>left+(W-left-right)*v/xMax;
  for(let t=0;t<=0.4001;t+=0.1){
    el('line',{x1:x(t),x2:x(t),y1:top-6,y2:H-bottom+4,stroke:line,'stroke-width':1},s);
    el('text',{x:x(t),y:H-bottom+22,'text-anchor':'middle','font-size':12,fill:muted,'font-family':'IBM Plex Mono,monospace'},s,num(t.toFixed(1)));
  }
  el('text',{x:left+(W-left-right)/2,y:H-4,'text-anchor':'middle','font-size':12,fill:muted},s,narrow?T('bits gained by the third preceding glyph','bit guadagnati dal terzo glifo precedente'):T('bits per glyph gained by the third preceding glyph','bit per glifo guadagnati dal terzo glifo precedente'));
  CORPORA.forEach((c,i)=>{
    const y=top+rowH*i+rowH/2+(narrow?8:0),col=css(c.fam),mn=Math.min(...c.gains),mx=Math.max(...c.gains);
    if(narrow)el('text',{x:left,y:y-15,'font-size':13,fill:ink,'font-weight':500},s,c.label+'  ·  '+fmt(mn)+'–'+fmt(mx));
    else el('text',{x:left-16,y:y+4,'text-anchor':'end','font-size':13.5,fill:ink,'font-weight':500},s,c.label);
    el('rect',{x:x(mn)-2,y:y-6,width:Math.max(4,x(mx)-x(mn)+4),height:12,rx:6,fill:col,opacity:.28},s);
    c.gains.forEach((g,k)=>{
      const dot=el('circle',{cx:x(g),cy:y,r:6,fill:col,stroke:css('--white'),'stroke-width':2},s);
      hover(dot,`<b>${c.label}</b><br>Split ${k+1}: ${fmt(g)} ${T('bits','bit')}`);
    });
    if(!narrow)el('text',{x:x(mx)+14,y:y+4,'font-size':12,fill:muted,'font-family':'IBM Plex Mono,monospace'},s,`${fmt(mn)}–${fmt(mx)}`);
  });
}

/* ---------- chart 1b: entropy curve ---------- */
function curveChart(host){
  const W=hostW(host),narrow=W<560,H=narrow?320:380,top=20,left=narrow?44:58,right=narrow?14:190,bottom=48;
  const s=svgRoot(host,W,H),muted=css('--muted'),line=css('--line'),ink=css('--ink');
  const yMin=1.8,yMax=4.2,x=o=>left+(W-left-right)*o/5,y=v=>top+(H-top-bottom)*(yMax-v)/(yMax-yMin);
  for(let v=2;v<=4.0001;v+=0.5){
    el('line',{x1:left,x2:W-right,y1:y(v),y2:y(v),stroke:line},s);
    el('text',{x:left-10,y:y(v)+4,'text-anchor':'end','font-size':12,fill:muted,'font-family':'IBM Plex Mono,monospace'},s,num(v.toFixed(1)));
  }
  for(let o=0;o<=5;o++)el('text',{x:x(o),y:H-bottom+22,'text-anchor':'middle','font-size':12,fill:muted,'font-family':'IBM Plex Mono,monospace'},s,o);
  el('text',{x:left+(W-left-right)/2,y:H-6,'text-anchor':'middle','font-size':12,fill:muted},s,narrow?T('model order','ordine del modello'):T('model order (number of preceding glyphs)','ordine del modello (glifi precedenti)'));
  el('text',{x:14,y:top+(H-top-bottom)/2,'text-anchor':'middle','font-size':12,fill:muted,transform:`rotate(-90 14 ${top+(H-top-bottom)/2})`},s,T('test entropy, bits per glyph','entropia sul test, bit per glifo'));
  // highlight the 2→3 step
  el('rect',{x:x(2),y:top,width:x(3)-x(2),height:H-top-bottom,fill:css('--lime'),opacity:.35},s);
  el('text',{x:(x(2)+x(3))/2,y:top+14,'text-anchor':'middle','font-size':11,fill:ink,'font-weight':600},s,'2 → 3');
  // end labels, nudged apart
  const ends=CORPORA.map(c=>({c,y:y(c.curve[5])})).sort((a,b)=>a.y-b.y);
  for(let i=1;i<ends.length;i++)if(ends[i].y-ends[i-1].y<16)ends[i].y=ends[i-1].y+16;
  CORPORA.forEach(c=>{
    const col=css(c.fam);
    el('path',{d:c.curve.map((v,o)=>(o?'L':'M')+x(o)+' '+y(v)).join(' '),fill:'none',stroke:col,'stroke-width':2.2,'stroke-dasharray':c.dash,'stroke-linejoin':'round'},s);
    c.curve.forEach((v,o)=>{
      const p=el('circle',{cx:x(o),cy:y(v),r:4.5,fill:col,stroke:css('--white'),'stroke-width':1.5},s);
      const hit=el('circle',{cx:x(o),cy:y(v),r:11,fill:'transparent'},s);
      hover(hit,`<b>${c.label}</b><br>${T('Order','Ordine')} ${o}: ${fmt(v)} ${T('bits','bit')}`);
    });
    const e=ends.find(z=>z.c===c);
    if(!narrow)el('text',{x:W-right+12,y:e.y+4,'font-size':12.5,fill:ink},s,c.label);
  });
}

/* ---------- chart 2: PCFG − HMM with interval ---------- */
function hierChart(host){
  const rows=[{label:'Voynich',fam:'--voynich',d:0.019291,lo:0.006544,hi:0.034324},
              {label:'Seraphinianus · OCR',fam:'--seraph',d:-0.003408,lo:-0.008042,hi:0.000793}];
  const W=hostW(host),narrow=W<560,rowH=narrow?66:56,top=narrow?24:16,left=narrow?14:190,right=narrow?16:40,bottom=44,H=top+rowH*rows.length+bottom;
  const s=svgRoot(host,W,H),muted=css('--muted'),line=css('--line'),ink=css('--ink');
  const lo=-0.015,hi=0.04,x=v=>left+(W-left-right)*(v-lo)/(hi-lo);
  for(let t=-0.01;t<=0.04001;t+=0.01){
    el('line',{x1:x(t),x2:x(t),y1:top-4,y2:H-bottom+4,stroke:Math.abs(t)<1e-9?ink:line,'stroke-width':Math.abs(t)<1e-9?1.5:1},s);
    el('text',{x:x(t),y:H-bottom+22,'text-anchor':'middle','font-size':12,fill:muted,'font-family':'IBM Plex Mono,monospace'},s,(narrow&&Math.round(t*100)%2?'':(t>0?'+':'')+num(t.toFixed(2))));
  }
  el('text',{x:x(0)-8,y:H-6,'text-anchor':'end','font-size':11.5,fill:muted},s,narrow?T('← tree better','← meglio l’albero'):T('← tree grammar better','← meglio la grammatica ad albero'));
  el('text',{x:x(0)+8,y:H-6,'font-size':11.5,fill:muted},s,narrow?T('chain better →','meglio la catena →'):T('chain model better →','meglio il modello a catena →'));
  rows.forEach((r,i)=>{
    const y=top+rowH*i+rowH/2+(narrow?8:0),col=css(r.fam);
    if(narrow)el('text',{x:left,y:y-17,'font-size':13,fill:ink,'font-weight':500},s,r.label+'  ·  '+(r.d>0?'+':'')+fmt(r.d));
    else el('text',{x:left-16,y:y+4,'text-anchor':'end','font-size':13.5,fill:ink,'font-weight':500},s,r.label);
    el('line',{x1:x(r.lo),x2:x(r.hi),y1:y,y2:y,stroke:col,'stroke-width':2.5},s);
    [r.lo,r.hi].forEach(v=>el('line',{x1:x(v),x2:x(v),y1:y-8,y2:y+8,stroke:col,'stroke-width':2.5},s));
    const d=el('circle',{cx:x(r.d),cy:y,r:7.5,fill:col,stroke:css('--white'),'stroke-width':2},s);
    hover(d,`<b>${r.label}</b><br>PCFG − HMM: ${(r.d>0?'+':'')+fmt(r.d)} ${T('bits/token','bit/token')}<br>${T('95% interval','intervallo al 95%')} [${fmt(r.lo)}, ${fmt(r.hi)}]`);
    if(!narrow)el('text',{x:x(r.hi)+12,y:y+4,'font-size':12,fill:muted,'font-family':'IBM Plex Mono,monospace'},s,(r.d>0?'+':'')+fmt(r.d));
  });
}

/* ---------- chart 3: substitution attack ---------- */
function subChart(host){
  const rows=[{label:T('Latin control','Controllo latino'),fam:'--control',v:68.60,n:T('933 / 1,360','933 / 1.360')},
              {label:T('Italian control','Controllo italiano'),fam:'--control',v:74.15,n:T('1,770 / 2,387','1.770 / 2.387')},
              {label:T('Voynich, Latin key','Voynich, chiave latina'),fam:'--voynich',v:1.11,n:T('35 / 3,153','35 / 3.153')},
              {label:T('Voynich, Italian key','Voynich, chiave italiana'),fam:'--voynich',v:7.01,n:T('221 / 3,153','221 / 3.153')}];
  const W=hostW(host),narrow=W<560,rowH=narrow?60:46,top=narrow?22:10,left=narrow?14:190,right=narrow?70:110,bottom=40,H=top+rowH*rows.length+bottom;
  const s=svgRoot(host,W,H),muted=css('--muted'),line=css('--line'),ink=css('--ink');
  const x=v=>left+(W-left-right)*v/100;
  for(let t=0;t<=100;t+=25){
    el('line',{x1:x(t),x2:x(t),y1:top,y2:H-bottom+4,stroke:line},s);
    el('text',{x:x(t),y:H-bottom+22,'text-anchor':'middle','font-size':12,fill:muted,'font-family':'IBM Plex Mono,monospace'},s,t+'%');
  }
  rows.forEach((r,i)=>{
    const y=top+rowH*i+(narrow?14:8),h=narrow?24:rowH-18,col=css(r.fam);
    if(narrow)el('text',{x:left,y:y-6,'font-size':13,fill:ink,'font-weight':500},s,r.label);
    else el('text',{x:left-16,y:y+h/2+4,'text-anchor':'end','font-size':13.5,fill:ink,'font-weight':500},s,r.label);
    const w=Math.max(4,x(r.v)-left);
    const b=el('path',{d:`M${left} ${y} H${left+w-4} a4 4 0 0 1 4 4 V${y+h-4} a4 4 0 0 1 -4 4 H${left} Z`,fill:col},s);
    hover(b,`<b>${r.label}</b><br>${num(r.v.toFixed(2))}% ${T('of words','delle parole')} (${r.n})`);
    el('text',{x:left+w+10,y:y+h/2+4,'font-size':12.5,fill:ink,'font-family':'IBM Plex Mono,monospace'},s,num(r.v.toFixed(2))+'%');
  });
}

/* ---------- wiring ---------- */
document.addEventListener('DOMContentLoaded',()=>{
  const g=document.getElementById('gain-chart');
  if(g){
    const gb=document.getElementById('gain-view'),cb=document.getElementById('curve-view');
    const title=document.getElementById('gain-title'),sub=document.getElementById('gain-sub');
    const show=mode=>{
      gb.classList.toggle('selected',mode==='gain');cb.classList.toggle('selected',mode==='curve');
      gb.setAttribute('aria-pressed',String(mode==='gain'));cb.setAttribute('aria-pressed',String(mode==='curve'));
      if(mode==='gain'){title.textContent=T('Gain from order 2 to order 3, bits per glyph','Guadagno dall’ordine 2 all’ordine 3, bit per glifo');sub.textContent=T('Each dot is one page split; the bar spans the lowest and highest split.','Ogni punto è uno split di pagine; la barra va dallo split più basso al più alto.');gainChart(g);}
      else{title.textContent=T('Test entropy by model order','Entropia sul test per ordine del modello');sub.textContent=T('Mean over three page splits. Dashed lines: second coding of the same family. The shaded band is the step measured above.','Media su tre split di pagine. Linee tratteggiate: seconda codifica della stessa famiglia. La fascia evidenziata è il passo misurato sopra.');curveChart(g);}
    };
    gb.addEventListener('click',()=>show('gain'));cb.addEventListener('click',()=>show('curve'));
    show('gain');
  }
  const h=document.getElementById('hier-chart');if(h)hierChart(h);
  const sc=document.getElementById('sub-chart');if(sc)subChart(sc);
  let lastW=innerWidth,t;
  addEventListener('resize',()=>{clearTimeout(t);t=setTimeout(()=>{if(Math.abs(innerWidth-lastW)<40)return;lastW=innerWidth;
    if(g)(document.getElementById('curve-view').classList.contains('selected')?curveChart:gainChart)(g);
    if(h)hierChart(h);if(sc)subChart(sc);},150);});
});
