'use strict';
// Beyond the Signs — Voynich Lab (lab.html). Depends on helpers defined in app.js
// (el, svgRoot, hostW, css, hover). All counts come from research/ outputs on ZL3b:
// voynich_full_inventory.json, voynich_inventory.json and patterns/results.json.

const UNITS={o:25619,e:20425,y:17879,a:14818,d:13215,i:11873,ch:11050,l:10658,k:10104,r:7595,n:6186,t:6017,q:5435,sh:4534,s:2822,p:1442,m:1071,cth:891,ckh:866,f:416,cph:201,g:154,cfh:67,x:41,v:15,b:15,j:14,c:12,u:9,z:9,h:4};
const UNITS_TOTAL=174004;
const CORE=['a','d','e','f','g','i','k','l','m','n','o','p','q','r','s','t','y','ch','sh','ckh','cth','cph','cfh'];

const RELATIONS={
  c:{n:11462,previous:{a:9,'^':6108,k:913,t:850,o:456,s:60,h:543,y:228,d:286,l:686,e:350,p:668,r:113,f:165,q:16,m:3,i:6,n:2},next:{h:9596,k:813,t:816,p:179,f:58}},
  h:{n:15517,previous:{c:9596,s:4054,k:811,t:816,p:179,f:58,h:2,y:1},next:{y:1917,o:3574,a:673,t:83,e:7333,i:4,'$':57,d:926,c:543,s:100,k:187,r:16,p:27,l:61,f:5,g:6,h:2,x:3}},
  q:{n:5087,previous:{'^':5061,o:14,y:11,l:1},next:{o:4987,k:16,e:51,y:7,c:16,a:6,f:1,s:2,p:1}},
  n:{n:5550,previous:{i:5439,a:101,e:1,o:5,'^':3,r:1},next:{'$':5493,y:12,o:20,l:2,d:5,s:2,g:1,a:11,c:2,k:1,p:1}}
};
const INSIGHT={
  q:'q almost only begins words (99.5%) and is followed by o 98% of the time. Few alphabetic letters behave like this; “qo” may be a single sign or a prefix.',
  n:'n comes after i 98% of the time and ends the word 99% of the time. Groups like in, iin and iiin look like one sign written with a variable number of strokes.',
  c:'In EVA, c almost never stands alone: it is followed by h 84% of the time. Transcribers therefore treat ch as one connected glyph.',
  h:'h is the second half of connected glyphs: it follows c or s in 88% of cases. On its own it is one of the rarest signs in the manuscript.'
};
const PREFIXES=['ok','qok','ot','qot','ch','sh'],SUFFIXES=['aiin','ain','edy','eedy','ol','ar'];
const FAMILY={ok:{aiin:166,ain:102,edy:80,eedy:76,ol:46,ar:90},qok:{aiin:220,ain:230,edy:209,eedy:244,ol:75,ar:117},ot:{aiin:118,ain:74,edy:110,eedy:69,ol:47,ar:98},qot:{aiin:58,ain:53,edy:66,eedy:63,ol:35,ar:52},ch:{aiin:37,ain:14,edy:383,eedy:41,ol:287,ar:54},sh:{aiin:16,ain:8,edy:335,eedy:64,ol:130,ar:25}};

const $=id=>document.getElementById(id);
function setSeg(buttons,active){buttons.forEach(b=>{b.classList.toggle('selected',b===active);b.setAttribute('aria-pressed',String(b===active));});}

/* ---------- 1. glyph frequencies ---------- */
function freqChart(host,coreOnly){
  const items=Object.entries(UNITS).filter(([k])=>!coreOnly||CORE.includes(k));
  const total=coreOnly?items.reduce((a,[,v])=>a+v,0):UNITS_TOTAL;
  const W=hostW(host),narrow=W<620,H=narrow?300:320,top=16,left=40,right=10,bottom=narrow?52:44;
  const s=svgRoot(host,W,H),muted=css('--muted'),line=css('--line'),ink=css('--ink');
  const max=16,y=v=>top+(H-top-bottom)*(1-v/max),bw=(W-left-right)/items.length;
  for(let t=0;t<=max;t+=4){
    el('line',{x1:left,x2:W-right,y1:y(t),y2:y(t),stroke:line},s);
    el('text',{x:left-8,y:y(t)+4,'text-anchor':'end','font-size':11.5,fill:muted,'font-family':'IBM Plex Mono,monospace'},s,t+'%');
  }
  items.forEach(([k,v],i)=>{
    const pct=100*v/total,x=left+bw*i,h=Math.max(1.5,y(0)-y(pct)),isCluster=k.length>1;
    const w=Math.max(2,bw-2),r=Math.min(4,w/2);
    const bar=el('path',{d:`M${x+1} ${y(0)} V${y(0)-h+r} a${r} ${r} 0 0 1 ${r} ${-r} H${x+1+w-r} a${r} ${r} 0 0 1 ${r} ${r} V${y(0)} Z`,fill:css('--voynich'),opacity:isCluster?.62:1},s);
    const hit=el('rect',{x:x,y:top,width:bw,height:H-top-bottom,fill:'transparent'},s);
    hover(hit,`<b>${k}</b>${isCluster?' (connected cluster)':''}<br>${v.toLocaleString('en')} glyphs · ${pct.toFixed(pct<0.1?3:2)}%`);
    if(!narrow||i%2===0||k.length===1)el('text',{x:x+bw/2,y:H-bottom+16,'text-anchor':'middle','font-size':narrow?10.5:12,fill:ink,'font-family':'IBM Plex Mono,monospace'},s,k);
  });
  el('text',{x:left,y:H-6,'font-size':11.5,fill:muted},s,'Lighter bars: connected clusters counted as one unit');
}

/* ---------- 2. neighbours ---------- */
const edgeLabel=k=>k==='^'?'word start':k==='$'?'word end':k;
function hbars(host,obj,total){
  host.innerHTML='';
  Object.entries(obj).sort((a,b)=>b[1]-a[1]).slice(0,8).forEach(([k,v])=>{
    const pct=100*v/total,row=document.createElement('div');row.className='hbar';
    row.innerHTML=`<span class="hbar-k ${k==='^'||k==='$'?'edge':''}">${edgeLabel(k)}</span><span class="hbar-track"><i style="width:${Math.max(.6,pct)}%"></i></span><span class="hbar-v">${pct.toFixed(1)}%</span>`;
    row.title=`${edgeLabel(k)}: ${v.toLocaleString('en')} of ${total.toLocaleString('en')}`;
    host.appendChild(row);
  });
}
function showNeighbours(g){
  const r=RELATIONS[g];
  $('nb-insight').textContent=INSIGHT[g];
  hbars($('nb-prev'),r.previous,r.n);hbars($('nb-next'),r.next,r.n);
}

/* ---------- 3. matrix ---------- */
function drawMatrix(share){
  const t=$('mx-table');t.innerHTML='';
  const head=t.createTHead().insertRow();head.insertCell().outerHTML='<th>start \\ ending</th>';
  SUFFIXES.forEach(sx=>head.insertCell().outerHTML=`<th class="num eva">-${sx}</th>`);
  const all=PREFIXES.flatMap(p=>SUFFIXES.map(sx=>FAMILY[p][sx])),max=Math.max(...all);
  const body=t.createTBody();
  PREFIXES.forEach(p=>{
    const row=body.insertRow(),rowSum=SUFFIXES.reduce((a,sx)=>a+FAMILY[p][sx],0);
    row.insertCell().outerHTML=`<th class="eva">${p}-</th>`;
    SUFFIXES.forEach(sx=>{
      const v=FAMILY[p][sx],sh=v/rowSum,level=share?sh/0.55:v/max;
      const c=row.insertCell();c.className='num mx-cell';
      c.style.setProperty('--a',Math.min(1,0.08+0.92*level).toFixed(3));
      c.classList.toggle('dark',level>0.5);
      c.textContent=share?(100*sh).toFixed(0)+'%':v;
      c.tabIndex=0;c.setAttribute('role','button');
      c.setAttribute('aria-label',`${p}${sx}: ${v} occurrences, ${(100*sh).toFixed(0)}% of the ${p}- row`);
      const pick=()=>{document.querySelectorAll('.mx-cell.on').forEach(x=>x.classList.remove('on'));c.classList.add('on');
        $('mx-readout').innerHTML=`<span class="eva" style="font-size:1.35em">${p}<b>${sx}</b></span> · ${v} occurrences · ${(100*sh).toFixed(1)}% of all <span class="eva">${p}-</span> words in this table`;};
      c.addEventListener('click',pick);c.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();pick();}});
    });
  });
}

/* ---------- 4. generator ---------- */
function weightedPick(pairs){let r=Math.random()*pairs.reduce((a,p)=>a+p[1],0);for(const p of pairs){r-=p[1];if(r<=0)return p[0];}return pairs[pairs.length-1][0];}
function generateLine(chain){
  const words=[];let prevEnd=null;
  for(let i=0;i<8;i++){
    const pairs=[];
    PREFIXES.forEach(p=>SUFFIXES.forEach(sx=>{
      let w=FAMILY[p][sx];
      // rule read off frequent pairs such as "shedy qokedy", "chedy qokain", "ol shedy", "ol chedy"
      if(chain&&prevEnd){
        if((prevEnd==='edy'||prevEnd==='eedy')&&p.startsWith('q'))w*=3;
        if((prevEnd==='ol'||prevEnd==='ar'||prevEnd==='ain')&&(p==='ch'||p==='sh'))w*=3;
      }
      pairs.push([[p,sx],w]);
    }));
    const [p,sx]=weightedPick(pairs);words.push(p+sx);prevEnd=sx;
  }
  return words;
}

/* ---------- 5. decipherment game ---------- */
const DEC_WORDS=[...PREFIXES.flatMap(p=>SUFFIXES.map(sx=>p+sx)),
  'daiin','aiin','or','al','dar','dal','chey','shey','s','r','qol','cthy','chor','cthor','dam','cheor','okeey','chy','cho','cthar','sheey','qokeey','ykeey','otal'];
const DEC_UNITS_ORDER=['cth','ch','sh','a','d','e','i','k','l','m','n','o','q','r','s','t','y'];
function tokenize(w){const out=[];let i=0;while(i<w.length){const u=['cth','ch','sh'].find(x=>w.startsWith(x,i))||w[i];out.push(u);i+=u.length;}return out;}
const DEC_TOK=DEC_WORDS.map(tokenize);
const DEC_UNITS=DEC_UNITS_ORDER.filter(u=>DEC_TOK.some(t=>t.includes(u)));
const LETTERS='abcdefghilmnopqrstuvxyz'.split('');
const DICT={
 latin:'a ab ad aer aes ait ala alia alio alius aliud alter ana anima ante aqua aquae ars arte at aut autem bene bona bonum bos cado caput causa celer certe cibus circa cito cor corpus cras cui cum cura dat de dea dei deus dic dies do domus dolor duo dum e ea eam eas edo ego eis eius eo ea ergo erat es esse est et etiam eum ex fac facit fit flos folia folium fons fuit gens habet hac haec herba hic hinc hoc hora hos huc iam ibi id idem ille illa in inde inter ipse ipsa ira is ita item iter iure ius lac latus lex locus luna lux magis male malum manus mare mater me mel meo mihi minus modo mons mora mors mos multa ne nec nihil nisi nobis non nos nox nunc ob odor oleum olim omnia omnis opus ora oro os pars pater per pes post pro quae quam quare qui quia quid quis quo quod quoque radix re rem res rex sal sanus sapor satis se sed semen semper si sic sine sit sol sola solus sub sua sui sum sunt suo super supra sus tam tamen te tela terra tibi tot totus tres tu tum ubi una unde unus ut uti vel vena venter via vir vis vita vos'.split(' '),
 italian:'a acqua ad aia al alla alto altra altro ama amico anche ancora anno ape aria arte casa che chi ci ciò come con cor cosa cosi cui da dal dalla dare dei del della di dice dio dire dito dopo dove due e ecco ed era erba essa esse essi esso fa fare fato fede fine fiore foglia ha hai hanno ho i il in io la lato lei lo loro lui luna ma madre male mano mare me mente mi mio mondo molto ne nei nel nella no noi non nome notte nuovo o occhio oggi olio ora ore oro padre pane parte per per poco poi pro qua quale quando qui re rete riso rosa sale sana se sei sera si sia sole solo sono sopra sotto su sua sue suo tale tanto te tela terra testa ti tra tre tu tutto uno uomo un una uno uva va vai vale vero vi via vino vita voi volta'.split(' ')
};
const DICT_SET={latin:new Set(DICT.latin),italian:new Set(DICT.italian)};
let decKey={};
function decode(tok){return tok.map(u=>decKey[u]||'·').join('');}
function decScore(lang){const d=DICT_SET[lang];let n=0;DEC_TOK.forEach(t=>{if(d.has(decode(t)))n++;});return n;}
function randomKey(){const pool=[...LETTERS].sort(()=>Math.random()-.5);decKey={};DEC_UNITS.forEach((u,i)=>decKey[u]=pool[i]);}
function renderDec(){
  const lang=$('dec-lang').value,d=DICT_SET[lang];
  const keyHost=$('dec-key');
  if(!keyHost.childElementCount){
    DEC_UNITS.forEach(u=>{
      const lab=document.createElement('label');lab.className='dec-slot';
      lab.innerHTML=`<span class="eva">${u}</span><select data-unit="${u}" aria-label="Letter for glyph ${u}">${LETTERS.map(l=>`<option>${l}</option>`).join('')}</select>`;
      keyHost.appendChild(lab);
      lab.querySelector('select').addEventListener('change',e=>{decKey[u]=e.target.value;renderDec();});
    });
  }
  keyHost.querySelectorAll('select').forEach(sel=>sel.value=decKey[sel.dataset.unit]);
  const wh=$('dec-words');wh.innerHTML='';let hits=0;
  DEC_TOK.forEach((t,i)=>{
    const out=decode(t),ok=d.has(out);if(ok)hits++;
    const span=document.createElement('span');span.className='dec-word'+(ok?' hit':'');
    span.innerHTML=`<small class="eva">${DEC_WORDS[i]}</small>${out}`;
    wh.appendChild(span);
  });
  $('dec-hits').textContent=hits;$('dec-total').textContent=DEC_WORDS.length;
}
function solve(){
  // hill climbing with restarts: maximise dictionary hits on these same words (deliberate overfitting)
  const lang=$('dec-lang').value;let best=null,bestS=-1;
  for(let r=0;r<12;r++){
    randomKey();let cur=decScore(lang);
    for(let it=0;it<2500;it++){
      const u=DEC_UNITS[Math.floor(Math.random()*DEC_UNITS.length)],old=decKey[u];
      const l=LETTERS[Math.floor(Math.random()*LETTERS.length)];
      const other=DEC_UNITS.find(v=>decKey[v]===l);
      decKey[u]=l;if(other)decKey[other]=old;
      const s=decScore(lang);
      if(s>=cur)cur=s;else{decKey[u]=old;if(other)decKey[other]=l;}
    }
    if(cur>bestS){bestS=cur;best={...decKey};}
  }
  decKey=best;renderDec();
  $('dec-lesson').classList.add('flash');setTimeout(()=>$('dec-lesson').classList.remove('flash'),1400);
}

/* ---------- 6. your text vs Voynich ---------- */
const SAMPLE_TEXT=()=>$('yt-input').defaultValue;
function stats(text){
  const words=text.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'').match(/[a-z]+/g)||[];
  const letters=words.join(''),freq={};for(const ch of letters)freq[ch]=(freq[ch]||0)+1;
  const n=letters.length;let h1=0;for(const k in freq){const p=freq[k]/n;h1-=p*Math.log2(p);}
  const triples=words.filter(w=>/(.)\1\1/.test(w)).length;
  const top=Object.values(freq).sort((a,b)=>b-a).slice(0,5).reduce((a,b)=>a+b,0);
  return {words:words.length,symbols:Object.keys(freq).length,h1,avg:n/Math.max(1,words.length),triples:100*triples/Math.max(1,words.length),top5:100*top/Math.max(1,n)};
}
function voyH1(){let h=0;for(const k in UNITS){const p=UNITS[k]/UNITS_TOTAL;h-=p*Math.log2(p);}return h;}
function renderYT(){
  const s=stats($('yt-input').value),vh=voyH1();
  const rows=[
    ['Words analysed',s.words.toLocaleString('en'),'32,888','—'],
    ['Distinct symbols used',s.symbols,'23 (working set)','No'],
    ['Entropy per symbol, from frequencies (bits)',s.h1.toFixed(2),vh.toFixed(2),'No'],
    ['Average word length (symbols)',s.avg.toFixed(2),'4.45','No'],
    ['Share taken by the 5 commonest symbols',s.top5.toFixed(1)+'%','52.8%','No'],
    ['Words with the same symbol three times in a row',s.triples.toFixed(1)+'%','1.0%','No']
  ];
  $('yt-table').innerHTML=rows.map(r=>`<tr><td>${r[0]}</td><td class="num">${r[1]}</td><td class="num">${r[2]}</td><td>${r[3]==='No'?'<span class="status green">No, identical</span>':''}</td></tr>`).join('');
}
function encipher(){
  const src='abcdefghijklmnopqrstuvwxyz'.split(''),dst=[...src].sort(()=>Math.random()-.5),m={};
  src.forEach((c,i)=>m[c]=dst[i]);
  const t=$('yt-input');
  t.value=t.value.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'').replace(/[a-z]/g,c=>m[c]);
  renderYT();
}

/* ---------- wiring ---------- */
document.addEventListener('DOMContentLoaded',()=>{
  const fc=$('freq-chart');if(!fc)return;
  const fa=$('freq-all'),fco=$('freq-core');let core=false;
  const drawF=()=>freqChart(fc,core);
  fa.addEventListener('click',()=>{core=false;setSeg([fa,fco],fa);drawF();});
  fco.addEventListener('click',()=>{core=true;setSeg([fa,fco],fco);drawF();});
  drawF();
  $('h1-voy').textContent=voyH1().toFixed(2);

  const gbtn=[...document.querySelectorAll('.glyph-pick button')];
  gbtn.forEach(b=>b.addEventListener('click',()=>{setSeg(gbtn,b);showNeighbours(b.dataset.glyph);}));
  showNeighbours('q');

  const mc=$('mx-count'),ms=$('mx-share');
  mc.addEventListener('click',()=>{setSeg([mc,ms],mc);drawMatrix(false);});
  ms.addEventListener('click',()=>{setSeg([mc,ms],ms);drawMatrix(true);});
  drawMatrix(false);

  const roll=()=>{const chain=$('gen-chain').checked,w=generateLine(chain);
    $('gen-line').innerHTML=w.map(x=>`<span>${x}</span>`).join(' ');
    $('gen-note').textContent=chain?'Each word above is a real Voynich word. Words after -edy favour q- starts, words after -ol, -ar, -ain favour ch- and sh-, as in frequent pairs such as shedy qokedy and ol chedy.':'Each word above is a real Voynich word. The line is not: start and ending were drawn independently.';};
  $('gen-go').addEventListener('click',roll);$('gen-chain').addEventListener('change',roll);roll();

  $('dec-nsym').textContent=DEC_UNITS.length;
  randomKey();renderDec();
  $('dec-random').addEventListener('click',()=>{randomKey();renderDec();});
  $('dec-solve').addEventListener('click',solve);
  $('dec-lang').addEventListener('change',renderDec);

  $('yt-input').addEventListener('input',renderYT);
  $('yt-cipher').addEventListener('click',encipher);
  $('yt-reset').addEventListener('click',()=>{$('yt-input').value=SAMPLE_TEXT();renderYT();});
  renderYT();

  let lw=innerWidth,tm;addEventListener('resize',()=>{clearTimeout(tm);tm=setTimeout(()=>{if(Math.abs(innerWidth-lw)<40)return;lw=innerWidth;drawF();},150);});
});
