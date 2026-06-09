const stocks=[
 {name:'NIFTY_AUTO',label:'Auto',price:26434.60,chg:1.60,type:'sector'},
 {name:'NIFTY_ENERGY',label:'Energy & Utilities',price:40520.85,chg:.70,type:'sector'},
 {name:'NIFTY_FIN_SERV',label:'Financials',price:25983.05,chg:1.77,type:'sector'},
 {name:'NIFTY_FMCG',label:'Consumer Staples',price:50247.80,chg:-.03,type:'sector'},
 {name:'NIFTY_INFRA',label:'Industrials',price:9442.25,chg:.88,type:'sector'},
 {name:'NIFTY_IT',label:'Information Technology',price:29038.90,chg:.44,type:'sector'},
 {name:'NIFTY_MEDIA',label:'Communications',price:1389.00,chg:1.05,type:'sector'},
 {name:'NIFTY_METAL',label:'Materials',price:13286.45,chg:.11,type:'sector'},
 {name:'NIFTY_PHARMA',label:'Health Care',price:24632.90,chg:.24,type:'sector'},
 {name:'NIFTY_REALTY',label:'Real Estate',price:786.25,chg:1.53,type:'sector'},
 {name:'AAPL',label:'Apple Inc',price:191.24,chg:1.24,type:'stock'},
 {name:'GOOGL',label:'Alphabet',price:173.60,chg:-.81,type:'stock'},
 {name:'TSLA',label:'Tesla',price:189.04,chg:2.11,type:'stock'},
 {name:'AMZN',label:'Amazon',price:184.98,chg:.64,type:'stock'},
 {name:'MSFT',label:'Microsoft',price:206.54,chg:-.32,type:'stock'},
 {name:'BTC',label:'Bitcoin',price:68420.10,chg:2.85,type:'crypto'},
];
const regions={
 US:[['Dow Jones','50,579.70','+0.58%'],['S&P 500','7,473.47','+0.37%'],['Nasdaq','26,343.97','+0.19%'],['Russell','2,869.23','+0.91%'],['VIX','16.70','-0.36%']],
 Europe:[['FTSE 100','9,876.10','+0.31%'],['DAX','24,560.25','+0.48%'],['CAC 40','8,931.50','-0.12%'],['STOXX 50','5,486.70','+0.22%']],
 India:[['NIFTY 50','23,963.10','+1.03%'],['SENSEX','76,282.47','+1.15%'],['Nifty Bank','55,016.10','+1.78%'],['Nifty IT','29,046.70','+0.46%']],
 Currencies:[['USD/INR','83.21','+0.09%'],['EUR/USD','1.08','-0.12%'],['GBP/USD','1.27','+0.05%'],['JPY/USD','156.21','-0.18%']],
 Crypto:[['Bitcoin','68,420.10','+2.85%'],['Ethereum','3,610.33','+1.49%'],['Solana','176.22','+4.29%'],['XRP','0.61','-0.45%']],
 Futures:[['Gold','2,431.20','+0.44%'],['Crude Oil','78.41','-1.20%'],['Silver','31.16','+0.80%'],['Natural Gas','2.91','+1.17%']]
};
const news=[
 ['Telangana Today','Sensex jumps over 900 points, Nifty surges amid fall in crude oil prices'],
 ['Markets Mojo',"Lloyds Engineering Works Ltd Surges 8.71% to Day's High"],
 ['Upstox','NIFTY50, SENSEX today: Asian markets, FII move, oil prices, key things to know'],
 ['The Economic Times','Nifty IT bottoming out? 2 stocks to buy this week'],
 ['ThePrint',"Ahmedabad's New Growth Roadmap: NSE-listed Laxmi Goldorna House Limited"],
 ['Equitymaster','Key Factors Behind Today’s Market Rally'],
 ['Mint','Oracle, Wipro, Tech Mahindra stocks fuel the Nifty IT index above 29,000'],
 ['Reuters',"India's IT shares near three-year low as OpenAI move revives AI fears"]
];
const questions=["What's going on with the markets today?","What is the impact of lower oil prices on Indian OMCs?","Which sectors are expected to perform best in the current week?"];
let current=stocks[1], watch=[], currentRegion='India', chartType='area', range='1D', compare=null, priceChart, riskChart;
const $=s=>document.querySelector(s); const $$=s=>[...document.querySelectorAll(s)];
function fmt(n){return Number(n).toLocaleString('en-IN',{maximumFractionDigits:2,minimumFractionDigits:2})}
function toast(t){const d=document.createElement('div');d.className='toast';d.textContent=t;$('#toastHost').appendChild(d);setTimeout(()=>d.remove(),2600)}
function modal(title,body){$('#modalTitle').textContent=title;$('#modalBody').innerHTML=body;$('#modal').classList.remove('hidden')}
function closeAllMenus(){['#addMenu','#chartTypeMenu','#compareMenu','#indicatorMenu','#searchResults'].forEach(x=>$(x)?.classList.add('hidden'))}
function series(base,n=80,vol=.015){let v=base,arr=[];for(let i=0;i<n;i++){v*=1+(Math.sin(i/6)*vol/2+(Math.random()-.48)*vol);arr.push(+v.toFixed(2))}return arr}
function labels(n=80){return Array.from({length:n},(_,i)=> i%10===0?`${9+Math.floor(i/20)}:${String((i*3)%60).padStart(2,'0')}`:'')}
function miniCanvas(vals){const w=82,h=35,max=Math.max(...vals),min=Math.min(...vals),pts=vals.map((v,i)=>`${i/(vals.length-1)*w},${h-(v-min)/(max-min||1)*h}`).join(' ');return `<svg class="spark" viewBox="0 0 ${w} ${h}"><polyline points="${pts}" fill="none" stroke="${vals.at(-1)>=vals[0]?'#8fed92':'#ff8fa0'}" stroke-width="2"/><linearGradient id="g"><stop offset="0" stop-color="#8fed92" stop-opacity=".4"/><stop offset="1" stop-color="#8fed92" stop-opacity="0"/></linearGradient></svg>`}
function renderSide(){function row(s){return `<div class="row-item ${s.name===current.name?'selected':''}" data-stock="${s.name}"><div><b>${s.name}</b><span class="sub">${s.label}</span></div>${miniCanvas(series(s.price,16,.012))}<div><b>${fmt(s.price)}</b><span class="${s.chg>=0?'green':'red'} sub">${s.chg>=0?'+':''}${s.chg.toFixed(2)}% ${s.chg>=0?'⬆':'⬇'}</span></div></div>`}
 $('#sectorList').innerHTML=stocks.filter(s=>s.type==='sector').map(row).join('');
 $('#marketList').innerHTML=['S&P 500','NASDAQ','Dow Jones','NIFTY 50','SENSEX','Bitcoin'].map((n,i)=>`<div class="row-item market-row" data-market="${n}"><div><b>${n}</b><span class="sub">Market index</span></div>${miniCanvas(series(100+i*20,16,.02))}<div><b>${fmt(1000+i*2200)}</b><span class="green sub">+${(.2+i/10).toFixed(2)}%</span></div></div>`).join('');
 renderWatch();
}
function renderWatch(){const box=$('#watchlistBox'); if(!watch.length){box.className='empty';box.innerHTML='This list is empty';return} box.className='list'; box.innerHTML=watch.map(n=>{const s=stocks.find(x=>x.name===n)||current;return `<div class="row-item" data-stock="${s.name}"><div><b>${s.name}</b><span class="sub">${s.label}</span></div>${miniCanvas(series(s.price,16,.012))}<div><b>${fmt(s.price)}</b><span class="${s.chg>=0?'green':'red'} sub">${s.chg>=0?'+':''}${s.chg.toFixed(2)}%</span></div></div>`}).join('')}
function renderHome(){const cards=regions[currentRegion]||regions.India;$('#marketCards').innerHTML=cards.map(c=>`<div class="market-card" data-market="${c[0]}"><h3>${c[0]}</h3><div class="value">${c[1]}</div><b class="${c[2][0]=='-'?'red':'green'}">${c[2]}</b>${miniCanvas(series(parseFloat(c[1].replace(/,/g,''))||100,30,.012))}</div>`).join('');
 $('#summaryTitle').textContent=currentRegion+' market summary';
 $('#summaryHeadline').textContent=currentRegion==='India'?'Domestic benchmarks rally on easing oil prices':`${currentRegion} markets show mixed momentum`;
 $('#summaryText').textContent=`${currentRegion} markets are being analysed by FinSight AI using price action, sector rotation, volatility, and news sentiment. Dashboard is demo-ready and all controls are interactive.`;
 $('#earningsList').innerHTML=['Suzlon Energy Limited','Fortis Healthcare Limited','Patanjali Foods Limited'].map((n,i)=>`<div class="earning"><div class="datebox"><b>${i?'TUE':'MON'}</b><br>${25+i}</div><div><b>${n}</b><span class="sub">Released · ${4+i}:00 pm UTC+5:30</span></div><div><span class="sub">EPS</span><br>₹${(i+0.32).toFixed(2)}</div><div><span class="sub">Rev</span><br>${(42-i*8).toFixed(2)}bn</div></div>`).join('');
 renderNews(false); renderMovers(); renderRisk();
}
function renderNews(more){$('#newsGrid').innerHTML=(more?news:news.slice(0,6)).map((n,i)=>`<div class="news" data-news="${i}"><small>🔴 ${n[0]} · ${15+i*8} minutes ago</small><b>${n[1]}</b></div>`).join('')}
function renderMovers(){const lists=[['#activeList',['IDEA','DAVANGERE','JPPOWER','FCL']],['#gainersList',['MODISONLTD','PREMEXPLN','HARIOMPIPE','JAYKAY']],['#losersList',['SATIA','GRADIENTE','SANSTAR','EXCELSOFT']]]; lists.forEach(([id,arr],k)=>$(id).innerHTML=arr.map((n,i)=>`<div class="stock-line"><div><b>${n}</b><span class="sub">Demo Ltd</span></div><b>₹${(13+i*100+k*50).toFixed(2)}</b><span class="${k==2?'red':'green'}">${k==2?'-':'+'}${(1+i*3.2).toFixed(2)}%</span></div>`).join(''))}
function renderRisk(){const ctx=$('#riskChart'); if(riskChart)riskChart.destroy(); riskChart=new Chart(ctx,{type:'radar',data:{labels:['Volatility','Momentum','Liquidity','Sentiment','Risk','Growth'],datasets:[{label:'AI Score',data:[70,84,76,62,48,79],fill:true}]},options:{plugins:{legend:{display:false}},scales:{r:{ticks:{display:false}}}}})}
function openDetail(s){current=s; $('#homeView').classList.add('hidden');$('#detailView').classList.remove('hidden');$('#tickerPath').textContent=s.name+':INDEXNSE';$('#detailName').textContent=s.label.includes('&')?'Nifty '+s.label.split(' ')[0]:s.name.startsWith('NIFTY_')?'Nifty '+s.label:s.label;$('#detailPrice').textContent=fmt(s.price);$('#detailChange').textContent=`${s.chg>=0?'+':''}${s.chg.toFixed(2)}% (${fmt(s.price*s.chg/100)}) Today`;$('#detailChange').className=s.chg>=0?'green':'red';$('#watchCheck').checked=watch.includes(s.name);renderOverview();renderPriceChart();$('#detailNews').innerHTML=news.slice(0,4).map((n,i)=>`<div class="news"><small>${n[0]} · ${i+1} hours ago</small><b>${n[1]}</b></div>`).join('');renderSide();}
function renderOverview(){const s=current, vals=[['Open',s.price*1.002],['Low',s.price*.997],['52-wk low',s.price*.81],['High',s.price*1.006],['52-wk high',s.price*1.022],['Volume',Math.round(s.price*1600)]];$('#overviewGrid').className='overview-grid';$('#overviewGrid').innerHTML=vals.map(v=>`<div class="ov"><span>${v[0]}</span><b>${fmt(v[1])}</b></div>`).join('')}
function chartColors(){const green=getComputedStyle(document.body).getPropertyValue('--green').trim()||'#8fed92';const red=getComputedStyle(document.body).getPropertyValue('--red').trim()||'#ff8fa0';const pos=current.chg>=0;return {line:pos?green:red,fill:pos?'rgba(143,237,146,.22)':'rgba(255,143,160,.22)',bar:pos?'rgba(143,237,146,.75)':'rgba(255,143,160,.75)'};}
function renderPriceChart(){const ctx=$('#priceChart');if(priceChart)priceChart.destroy();let n=range==='1D'?80:range==='5D'?120:160;let vals=series(current.price,n,range==='1D'?.006:.018);let c=chartColors();let datasets=[{label:current.name,data:vals,borderWidth:2,tension:.25,fill:chartType==='area',borderColor:c.line,backgroundColor:chartType==='bar'?c.bar:c.fill,pointBackgroundColor:c.line,pointBorderColor:c.line}];if(compare){datasets.push({label:compare,data:series(current.price*.94,n,.012),borderWidth:2,tension:.25,fill:false,borderColor:'#8ea7ff',backgroundColor:'rgba(142,167,255,.18)'});}let graphType=chartType==='bar'?'bar':'line';priceChart=new Chart(ctx,{type:graphType,data:{labels:labels(n),datasets:datasets},options:{responsive:true,maintainAspectRatio:false,interaction:{mode:'index',intersect:false},plugins:{legend:{display:true,labels:{color:getComputedStyle(document.body).getPropertyValue('--muted')}}},scales:{x:{ticks:{color:getComputedStyle(document.body).getPropertyValue('--muted')},grid:{color:'rgba(150,150,150,.12)'}},y:{ticks:{color:getComputedStyle(document.body).getPropertyValue('--muted')},grid:{color:'rgba(150,150,150,.12)'}}}}});$('#chartTypeBtn').textContent=(chartType==='area'?'▰ Area':chartType==='line'?'⌁ Line':chartType==='candle'?'▥ Candle':'▮ Bar')+' ▾';}
function ask(q){const chat=$('#assistantChat');chat.innerHTML+=`<div class="msg user">${q}</div>`;let ans=`FinSight AI analysis: ${q} — current selected asset is ${current.name}. Trend is ${current.chg>=0?'bullish':'bearish'}, price ${fmt(current.price)}, change ${current.chg.toFixed(2)}%. Suggested action: check volatility, support/resistance and news before decision.`;chat.innerHTML+=`<div class="msg">${ans}</div>`;chat.scrollTop=chat.scrollHeight}
function search(q){q=q.toLowerCase();const res=stocks.filter(s=>(s.name+s.label).toLowerCase().includes(q)).slice(0,8);const box=$('#searchResults');if(!q||!res.length){box.classList.add('hidden');return}box.innerHTML=res.map(s=>`<div class="search-result" data-stock="${s.name}"><div><b>${s.name}</b><span class="sub">${s.label}</span></div><span class="${s.chg>=0?'green':'red'}">${s.chg>=0?'+':''}${s.chg}%</span></div>`).join('');box.classList.remove('hidden')}

function setUserName(name){
  const clean=(name||'').trim();
  if(!clean) return;
  localStorage.setItem('finsight_user_name',clean);
  $('#profileBtn').textContent=clean[0].toUpperCase();
  $('#researchGreeting').textContent=`Hi ${clean}, ask any financial question`;
}
function loadUserName(){
  const name=localStorage.getItem('finsight_user_name');
  if(name) setUserName(name); else $('#researchGreeting').textContent='Hi, ask any financial question';
}
function openGoogleProfile(){
  modal('Google Profile Login',`<div class="google-login-card"><div class="google-g">G</div><div><b>Continue with Google</b><p class="sub">For real Google login, add your Google OAuth Client ID in a hosted version. This button opens Google sign-in page.</p></div></div><button class="pill active" id="googleOpenBtn">Open Google Sign-in</button><hr style="border:0;border-top:1px solid var(--line);margin:18px 0"><p><b>Demo login for project presentation</b></p><input id="demoNameInput" class="profile-input" placeholder="Enter your name, e.g. Tanu"><br><br><button class="pill active" id="saveDemoNameBtn">Save name in dashboard</button>`);
  setTimeout(()=>{
    const g=$('#googleOpenBtn'), save=$('#saveDemoNameBtn');
    if(g) g.onclick=()=>window.open('https://accounts.google.com/','_blank');
    if(save) save.onclick=()=>{setUserName($('#demoNameInput').value);$('#modal').classList.add('hidden');toast('Profile updated')};
  },0);
}

function bind(){document.addEventListener('click',e=>{const st=e.target.closest('[data-stock]'); if(st){openDetail(stocks.find(s=>s.name===st.dataset.stock)||current);closeAllMenus()} const m=e.target.closest('[data-market]');if(m){modal('Market Selected',`<p>${m.dataset.market} market page loaded. In this demo it updates research and market sentiment.</p>`);ask(`Analyse ${m.dataset.market}`)} const n=e.target.closest('[data-news]');if(n)modal('News Story',`<p>${news[n.dataset.news][1]}</p><p class="sub">This is a demo news detail view with AI summarisation.</p>`)});$('#homeLogo').onclick=()=>{$('#detailView').classList.add('hidden');$('#homeView').classList.remove('hidden')};$('#backHome').onclick=$('#homeLogo').onclick;$('#themeBtn').onclick=()=>{document.body.classList.toggle('light');renderPriceChart();toast('Theme changed')};$('#collapseSidebarBtn').onclick=()=>document.body.classList.toggle('sidebar-collapsed');$('#expandResearchBtn').onclick=()=>document.body.classList.toggle('full-research');$('#profileBtn').onclick=()=>openGoogleProfile();$('#feedbackBtn').onclick=()=>modal('Send feedback to FinSight AI',`<label class="feedback-label">Describe your feedback</label><textarea class="feedback-text" placeholder="Tell us what should be improved..."></textarea><p class="sub">A screenshot or short description will help improve this student project.</p><button class="pill active" onclick="document.getElementById('modal').classList.add('hidden')">Send feedback</button>`);$('#addListBtn').onclick=()=>modal('New List','<input id="newListName" placeholder="List name" style="width:100%;padding:12px;border-radius:12px;background:var(--panel2);border:1px solid var(--line)"><br><br><button class="pill active" onclick="document.getElementById(\'modal\').classList.add(\'hidden\')">Create</button>');$('#addWatchBtn').onclick=()=>{if(!watch.includes(current.name))watch.push(current.name);renderWatch();toast(current.name+' added to watchlist')};$('#learnMoreLink').onclick=()=>modal('About FinSight AI','<p>FinSight AI is a student project for stock market dashboard, AI research, trend visualisation and watchlist analysis.</p>');$('#modalClose').onclick=()=>$('#modal').classList.add('hidden');$('#modal').onclick=e=>{if(e.target.id==='modal')$('#modal').classList.add('hidden')};$$('[data-toggle]').forEach(b=>b.onclick=()=>$('#'+b.dataset.toggle).classList.toggle('hidden')); $$('#regionTabs button').forEach(b=>b.onclick=()=>{$$('#regionTabs button').forEach(x=>x.classList.remove('active'));b.classList.add('active');currentRegion=b.dataset.region;renderHome();toast(currentRegion+' market loaded')});$('#diveBtn').onclick=()=>ask($('#summaryHeadline').textContent);$$('.acc').forEach(a=>a.onclick=()=>a.nextElementSibling.classList.toggle('open'));$('#moreEarnings').onclick=()=>modal('Upcoming Earnings','<p>More demo earnings calendar opened. Add-to-calendar and alerts are enabled visually.</p>');let more=false;$('#showMoreNews').onclick=()=>{more=!more;renderNews(more);$('#showMoreNews').textContent=more?'Show fewer ⌃':'Show more ⌄'};$('#addCurrentBtn').onclick=e=>{$('#addMenu').classList.toggle('hidden');e.stopPropagation()};$('#newListBtn').onclick=()=>toast('New watchlist created');$('#doneListBtn').onclick=()=>{$('#addMenu').classList.add('hidden');toast('Watchlist saved')};$('#watchCheck').onchange=e=>{if(e.target.checked&&!watch.includes(current.name))watch.push(current.name); if(!e.target.checked)watch=watch.filter(x=>x!==current.name);renderWatch()};$('#chartTypeBtn').onclick=e=>{$('#chartTypeMenu').classList.toggle('hidden');e.stopPropagation()};$$('[data-chart-type]').forEach(b=>b.onclick=()=>{chartType=b.dataset.chartType;renderPriceChart();closeAllMenus();toast('Chart changed to '+chartType)});$('#compareBtn').onclick=e=>{$('#compareMenu').classList.toggle('hidden');e.stopPropagation()};$$('[data-compare]').forEach(b=>b.onclick=()=>{compare=b.dataset.compare;renderPriceChart();closeAllMenus();toast('Compared with '+compare)});$('#indicatorBtn').onclick=e=>{$('#indicatorMenu').classList.toggle('hidden');e.stopPropagation()};$$('[data-indicator]').forEach(i=>i.onchange=()=>toast('Indicator updated'));$$('#rangeTabs button').forEach(b=>b.onclick=()=>{$$('#rangeTabs button').forEach(x=>x.classList.remove('active'));b.classList.add('active');range=b.dataset.range;renderPriceChart()});$('#betaBtn').onclick=()=>toast('Beta mode already active');$('#searchInput').oninput=e=>search(e.target.value);$('#searchInput').onkeydown=e=>{if(e.key==='Enter'){let s=stocks.find(x=>(x.name+x.label).toLowerCase().includes(e.target.value.toLowerCase())); if(s)openDetail(s)}};$('#composeBtn').onclick=()=>{$('#askInput').focus();toast('Write your financial question')};$('#historyBtn').onclick=()=>modal('Research History','<p>Recent: market trend, watchlist analysis, sector rotation, volatility check.</p>');$('#attachBtn').onclick=()=>toast('Attachment option clicked');$('#sendAskBtn').onclick=()=>{let q=$('#askInput').value.trim();if(q){ask(q);$('#askInput').value=''}};$('#askInput').onkeydown=e=>{if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();$('#sendAskBtn').click()}};$('#questionList').innerHTML=questions.map(q=>`<button class="qbtn">${q}<span>⌕</span></button>`).join('');$$('.qbtn').forEach(b=>b.onclick=()=>{$$('.qbtn').forEach(x=>x.classList.remove('active'));b.classList.add('active');ask(b.textContent.replace('⌕','').trim())});$$('.explore').forEach(b=>b.onclick=()=>{$$('.explore').forEach(x=>x.classList.remove('active'));b.classList.add('active');ask(b.textContent.trim())});document.addEventListener('click',e=>{if(!e.target.closest('.dropdown')&&!e.target.closest('.chart-toolbar')&&!e.target.closest('.detail-actions')&&!e.target.closest('.search-wrap'))closeAllMenus()})}
function tick(){stocks.forEach(s=>{s.price*=1+(Math.random()-.48)*.0008}); if(!$('#detailView').classList.contains('hidden')){ $('#detailPrice').textContent=fmt(current.price); } renderSide();}
renderSide();renderHome();bind();loadUserName();openDetail(stocks[1]);$('#detailView').classList.add('hidden');$('#homeView').classList.remove('hidden');setInterval(tick,3500);
/* =====================================================
   FINSIGHT AI — HOVER TOOLTIPS
   ===================================================== */

// ---- Tooltip singleton ----
(function () {
  const TT = document.createElement('div');
  TT.className = 'finsight-tooltip';
  document.body.appendChild(TT);

  let hideTimer = null;

  function showTT(html, x, y) {
    clearTimeout(hideTimer);
    TT.innerHTML = html;
    // Keep tooltip inside viewport
    const vw = window.innerWidth, vh = window.innerHeight;
    const tw = 240, th = 150;
    let left = x + 16, top = y + 14;
    if (left + tw > vw - 12) left = x - tw - 12;
    if (top + th > vh - 12) top = y - th - 12;
    TT.style.left = left + 'px';
    TT.style.top  = top  + 'px';
    TT.classList.add('tt-visible');
  }

  function hideTT() {
    hideTimer = setTimeout(() => TT.classList.remove('tt-visible'), 80);
  }

  // ---- Tooltip data definitions ----
  const sectorTooltips = {
    NIFTY_AUTO:    { desc: 'Automobile & components', pe: '28.4', cap: '₹14.2T', week52: '19,840 – 28,610' },
    NIFTY_ENERGY:  { desc: 'Energy & utilities sector', pe: '22.1', cap: '₹26.8T', week52: '30,100 – 44,780' },
    NIFTY_FIN_SERV:{ desc: 'Banking & financial services', pe: '19.6', cap: '₹58.1T', week52: '19,520 – 27,930' },
    NIFTY_FMCG:    { desc: 'Fast-moving consumer goods', pe: '43.2', cap: '₹19.7T', week52: '46,410 – 56,090' },
    NIFTY_INFRA:   { desc: 'Infrastructure & industrials', pe: '31.5', cap: '₹8.6T',  week52: '7,210 – 10,660' },
    NIFTY_IT:      { desc: 'Information technology', pe: '26.8', cap: '₹32.4T', week52: '22,910 – 32,460' },
    NIFTY_MEDIA:   { desc: 'Broadcasting & media', pe: '41.0', cap: '₹1.1T',  week52: '1,110 – 1,890' },
    NIFTY_METAL:   { desc: 'Metals & mining', pe: '17.3', cap: '₹9.2T',  week52: '9,820 – 16,140' },
    NIFTY_PHARMA:  { desc: 'Pharmaceuticals & biotech', pe: '35.6', cap: '₹15.8T', week52: '18,230 – 27,410' },
    NIFTY_REALTY:  { desc: 'Real estate & REITs', pe: '52.1', cap: '₹2.4T',  week52: '570 – 1,160' },
  };

  const earningsTooltips = {
    'Suzlon Energy Limited':     { ticker: 'SUZLON', sector: 'Renewable Energy', eps: '₹0.32', rev: '₹42bn', yoy: '+18%', analyst: 'Outperform' },
    'Fortis Healthcare Limited': { ticker: 'FORTIS',  sector: 'Hospitals',       eps: '₹1.32', rev: '₹34bn', yoy: '+11%', analyst: 'Hold' },
    'Patanjali Foods Limited':   { ticker: 'PATANJALI',sector: 'FMCG',           eps: '₹2.32', rev: '₹26bn', yoy: '+6%',  analyst: 'Buy' },
  };

  const marketTooltips = {
    'NIFTY 50':    { desc: 'Top 50 large-cap Indian stocks', exchange: 'NSE', type: 'Index' },
    'SENSEX':      { desc: '30 blue-chip stocks on BSE', exchange: 'BSE', type: 'Index' },
    'Nifty Bank':  { desc: 'Top 12 liquid banking stocks', exchange: 'NSE', type: 'Sectoral' },
    'Nifty IT':    { desc: 'IT sector large-cap index', exchange: 'NSE', type: 'Sectoral' },
    'Dow Jones':   { desc: '30 large US blue-chip companies', exchange: 'NYSE', type: 'Index' },
    'S&P 500':     { desc: '500 leading US companies', exchange: 'NYSE/NASDAQ', type: 'Index' },
    'Nasdaq':      { desc: 'Tech-heavy US composite index', exchange: 'NASDAQ', type: 'Index' },
  };

  function sectorHTML(name, s) {
    return `<div class="tt-title">${name}</div>
      <div class="tt-row"><span>Sector</span><b>${s.desc}</b></div>
      <div class="tt-row"><span>P/E Ratio</span><b>${s.pe}</b></div>
      <div class="tt-row"><span>Mkt Cap</span><b>${s.cap}</b></div>
      <div class="tt-row"><span>52-wk range</span><b>${s.week52}</b></div>
      <button class="tt-explore-btn">Click to explore \u203a</button>`;
  }

  function earningsHTML(name, e) {
    return `<div class="tt-title">${name}</div>
      <div class="tt-row"><span>Ticker</span><b>${e.ticker}</b></div>
      <div class="tt-row"><span>Sector</span><b>${e.sector}</b></div>
      <div class="tt-row"><span>EPS Est.</span><b>${e.eps}</b></div>
      <div class="tt-row"><span>Rev Est.</span><b>${e.rev}</b></div>
      <div class="tt-row"><span>YoY Growth</span><b>${e.yoy}</b></div>
      <div class="tt-row"><span>Analyst</span><b>${e.analyst}</b></div>
      <button class="tt-explore-btn">Click to explore \u203a</button>`;
  }

  function marketHTML(name, m) {
    return `<div class="tt-title">${name}</div>
      <div class="tt-row"><span>Description</span><b>${m.desc}</b></div>
      <div class="tt-row"><span>Exchange</span><b>${m.exchange}</b></div>
      <div class="tt-row"><span>Type</span><b>${m.type}</b></div>
      <span class="tt-badge">View details ›</span>`;
  }

  // ---- Event delegation for dynamically rendered items ----
  document.addEventListener('mousemove', e => {
    const row = e.target.closest('.row-item');
    const ear = e.target.closest('.earning');
    const mkt = e.target.closest('[data-market]');
    const mc  = e.target.closest('.market-card');

    if (row) {
      // Sector or market list row
      const nameEl = row.querySelector('b');
      if (!nameEl) return;
      const name = nameEl.textContent.trim();
      // Try sector first
      const sKey = Object.keys(sectorTooltips).find(k => name.includes(k) || row.textContent.includes(k));
      if (sKey) { showTT(sectorHTML(sKey, sectorTooltips[sKey]), e.clientX, e.clientY); return; }
      // Try market index
      const mKey = Object.keys(marketTooltips).find(k => name.includes(k));
      if (mKey) { showTT(marketHTML(mKey, marketTooltips[mKey]), e.clientX, e.clientY); return; }
      hideTT();
      return;
    }

    if (ear) {
      // The first <b> is inside .datebox (MON/TUE) — skip it, get the company name <b>
      const nameEl = ear.querySelector('div:not(.datebox) b');
      if (!nameEl) { hideTT(); return; }
      const name = nameEl.textContent.trim();
      const eKey = Object.keys(earningsTooltips).find(k => k === name || name.includes(k) || k.includes(name));
      if (eKey) { showTT(earningsHTML(eKey, earningsTooltips[eKey]), e.clientX, e.clientY); return; }
      hideTT();
      return;
    }

    if (mc) {
      const h3 = mc.querySelector('h3');
      if (!h3) { hideTT(); return; }
      const name = h3.textContent.trim();
      const mKey = Object.keys(marketTooltips).find(k => name.includes(k) || k.includes(name));
      if (mKey) { showTT(marketHTML(mKey, marketTooltips[mKey]), e.clientX, e.clientY); return; }
      hideTT();
      return;
    }

    hideTT();
  });

  document.addEventListener('mouseleave', hideTT, true);
})();

/* =====================================================
   PANEL RESIZE HANDLES — sidebar & research
   ===================================================== */
(function () {
  const shell    = document.querySelector('.app-shell');
  const sidebarH = document.getElementById('sidebarHandle');
  const researchH= document.getElementById('researchHandle');

  // Parse current grid cols → returns array of 5 pixel values
  // cols: [sidebar, handle, main, handle, research]
  function getCols() {
    const raw = getComputedStyle(shell).gridTemplateColumns;
    return raw.split(' ').map(v => parseFloat(v) || 0);
  }

  function setGrid(sidebarW, researchW) {
    shell.style.gridTemplateColumns =
      `${sidebarW}px 8px 1fr 8px ${researchW}px`;
  }

  function setupHandle(handle, panelIndex) {
    if (!handle) return;

    handle.addEventListener('mousedown', function (e) {
      e.preventDefault();
      const startX  = e.clientX;
      const cols     = getCols();
      // cols[0]=sidebar, cols[4]=research
      const startSidebar  = cols[0];
      const startResearch = cols[4];

      handle.classList.add('rh-dragging');
      document.body.classList.add('rh-resizing');

      function onMove(e) {
        const dx = e.clientX - startX;

        if (panelIndex === 0) {
          // Sidebar handle — drag right = wider sidebar
          const newSidebar = Math.max(180, Math.min(540, startSidebar + dx));
          setGrid(newSidebar, startResearch);
        } else {
          // Research handle — drag left = wider research
          const newResearch = Math.max(280, Math.min(860, startResearch - dx));
          setGrid(startSidebar, newResearch);
        }
      }

      function onUp() {
        handle.classList.remove('rh-dragging');
        document.body.classList.remove('rh-resizing');
        document.removeEventListener('mousemove', onMove);
        document.removeEventListener('mouseup',   onUp);
      }

      document.addEventListener('mousemove', onMove);
      document.addEventListener('mouseup',   onUp);
    });

    // Double-click to reset panel to default width
    handle.addEventListener('dblclick', function () {
      const cols = getCols();
      if (panelIndex === 0) {
        setGrid(310, cols[4]);
      } else {
        setGrid(cols[0], 610);
      }
      if (typeof toast === 'function') toast('Panel reset to default');
    });
  }

  setupHandle(sidebarH,  0);   // sidebar / equity sectors
  setupHandle(researchH, 4);   // research panel
})();
