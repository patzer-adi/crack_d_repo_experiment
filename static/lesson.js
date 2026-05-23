function toggleEl(id,btn){const el=document.getElementById(id);const open=el.classList.toggle('open');if(btn)btn.textContent=open?'▼ Hide Code':'▶ Reveal Code';}
function switchTab(idx){[0,1,2].forEach(i=>{const t=document.getElementById('tab'+i),p=document.getElementById('pane'+i);if(t)t.classList.toggle('active',i===idx);if(p)p.classList.toggle('active',i===idx);});}

function cvBuildCode(lines){
  const p=document.getElementById('cv-code-panel'); p.innerHTML='';
  lines.forEach(l=>{
    const d=document.createElement('div'); d.className='cv-line'; d.id='cvL'+l.n;
    const num=document.createElement('span'); num.className='cv-line-num'; num.textContent=l.n;
    const code=document.createElement('span'); code.className='cv-line-code'; code.textContent=l.c;
    d.appendChild(num); d.appendChild(code); p.appendChild(d);
  });
}

function cvStopPlay(){clearInterval(cvTimer);cvTimer=null;document.getElementById('cv-bplay').textContent='▶ Auto';}
function cvTogglePlay(){if(cvTimer){cvStopPlay();}else{document.getElementById('cv-bplay').textContent='⏸ Pause';cvTimer=setInterval(()=>{if(cvCur<cvSteps.length-1)cvNext();else cvStopPlay();},1400);}}
function drStopPlay(){clearInterval(drTimer);drTimer=null;document.getElementById('dr-bplay').textContent='▶ Auto';}
function drTogglePlay(){if(drTimer){drStopPlay();}else{document.getElementById('dr-bplay').textContent='⏸ Pause';drTimer=setInterval(()=>{if(drCur<drSteps.length-1)drNext();else drStopPlay();},1400);}}
function bfStopPlay(){clearInterval(bfTimer);bfTimer=null;document.getElementById('bf-play').textContent='▶ Auto';}
function bfTogglePlay(){if(bfTimer){bfStopPlay();}else{document.getElementById('bf-play').textContent='⏸ Pause';bfTimer=setInterval(()=>{if(bfCur<bfSteps.length-1)bfNext();else bfStopPlay();},1400);}}

function visPx(el){if(!el)return 0;const r=el.getBoundingClientRect(),vh=window.innerHeight;return Math.max(0,Math.min(r.bottom,vh)-Math.max(r.top,0));}
document.addEventListener('keydown',e=>{
  if(e.target.tagName==='INPUT'||e.target.tagName==='TEXTAREA') return;
  const useCv=visPx(document.querySelector('.cv-section'))>visPx(document.querySelector('.dr-section'));
  if(e.key==='ArrowLeft'){e.preventDefault();useCv?cvPrev():drPrev();}
  if(e.key==='ArrowRight'){e.preventDefault();useCv?cvNext():drNext();}
  if(e.key===' '){e.preventDefault();useCv?cvTogglePlay():drTogglePlay();}
  if(e.key==='r'||e.key==='R'||e.key==='Escape'){useCv?cvReset():drReset();}
});
