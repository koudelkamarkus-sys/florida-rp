(()=>{
 const root=document.documentElement;
 const preference=matchMedia('(prefers-reduced-motion: reduce)');
 const compact=matchMedia('(max-width: 800px)');
 const toggle=document.querySelector('.motion-toggle');
 let paused=false;
 try{paused=localStorage.getItem('florida-rp-motion')==='off'}catch{}
 const targets=document.querySelectorAll('.section-head,.feature,.membership>div,.faq>div, .contact,.scene-copy,.scenario-card');
 if('IntersectionObserver' in window){
  const observer=new IntersectionObserver(entries=>entries.forEach(entry=>{if(entry.isIntersecting){entry.target.classList.add('is-visible');observer.unobserve(entry.target)}}),{threshold:.08});
  targets.forEach((element,index)=>{element.classList.add('reveal');if(element.classList.contains('feature'))element.style.setProperty('--delay',`${index%3*90}ms`);observer.observe(element)});
  root.classList.add('motion-ready');
 }
 const hero=document.querySelector('.hero');
 const scene=document.querySelector('.scene');
 const progress=document.querySelector('.scroll-progress');
 const sections=[...document.querySelectorAll('#community,#scenarios,#membership,#faq')];
 const links=[...document.querySelectorAll('nav a')];
 let queued=false;
 function draw(){
  queued=false;
  const y=window.scrollY;
  const max=document.documentElement.scrollHeight-innerHeight;
  progress.style.transform=`scaleX(${max>0?Math.min(1,y/max):0})`;
  const moving=!paused&&!preference.matches&&!compact.matches;
  hero.style.setProperty('--shift',moving?`${Math.min(y*.13,85)}px`:'0px');
  const bounds=scene.getBoundingClientRect();
  const displacement=Math.max(-55,Math.min(55,(innerHeight/2-bounds.top-bounds.height/2)*.12));
  scene.style.setProperty('--scene-shift',moving?`${displacement}px`:'0px');
  let active='';for(const section of sections){if(section.getBoundingClientRect().top<innerHeight*.45)active=section.id}
  links.forEach(link=>{if(link.getAttribute('href')==='#'+active)link.setAttribute('aria-current','location');else link.removeAttribute('aria-current')});
 }
 function requestDraw(){if(!queued){queued=true;requestAnimationFrame(draw)}}
 function settings(){root.classList.toggle('motion-paused',paused||preference.matches);toggle.textContent=paused||preference.matches?'Motion: off':'Motion: on';toggle.setAttribute('aria-pressed',String(!(paused||preference.matches)));requestDraw()}
 toggle.addEventListener('click',()=>{paused=!paused;try{localStorage.setItem('florida-rp-motion',paused?'off':'on')}catch{}settings()});
 preference.addEventListener('change',settings);compact.addEventListener('change',requestDraw);
 addEventListener('scroll',requestDraw,{passive:true});addEventListener('resize',requestDraw);settings();
})();

