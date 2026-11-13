(()=>{
 const canvas=document.createElement('canvas');canvas.className='window-rain';canvas.setAttribute('aria-hidden','true');document.body.append(canvas);
 const ctx=canvas.getContext('2d');if(!ctx){canvas.remove();return}
 const reduced=matchMedia('(prefers-reduced-motion: reduce)');let w=0,h=0,drops=[],beads=[],frame=0,last=0,next=0;
 let seed=23017;function random(){seed=(seed*16807)%2147483647;return(seed-1)/2147483646}
 function drop(top=false){const r=3.0+random()**1.6*4.0;return{x:random()*w,y:top?-25:random()*h,r,v:0,wait:2+random()*12,phase:random()*6.28,skew:(random()-.5)*.35,trail:[]}}
 function resize(){w=innerWidth;h=innerHeight;const d=Math.min(devicePixelRatio||1,1.5);canvas.width=Math.round(w*d);canvas.height=Math.round(h*d);ctx.setTransform(d,0,0,d,0,0);seed=23017;drops=Array.from({length:Math.round(Math.min(68,w*h/21000))},()=>drop());beads=Array.from({length:Math.min(340,Math.round(w*h/4100))},()=>({x:random()*w,y:random()*h,r:.5+random()**2*2.0}));ctx.clearRect(0,0,w,h)}
 function enabled(){return!document.hidden&&!reduced.matches&&!document.documentElement.classList.contains('motion-paused')}
 function outline(d){const r=d.r,s=1+Math.min(d.v/120,.55);ctx.beginPath();ctx.moveTo(d.x,d.y-r*s);ctx.bezierCurveTo(d.x+r*.80,d.y-r*s*.94,d.x+r*1.06,d.y-r*.10,d.x+r*.86,d.y+r*.72);ctx.bezierCurveTo(d.x+r*.52,d.y+r*1.22,d.x-r*.58,d.y+r*1.18,d.x-r*.91,d.y+r*.52);ctx.bezierCurveTo(d.x-r*1.02,d.y-r*.24,d.x-r*.66,d.y-r*s,d.x,d.y-r*s);ctx.closePath()}
 function paint(t){
  frame=0;if(!enabled()){ctx.clearRect(0,0,w,h);last=0;return}frame=requestAnimationFrame(paint);if(t<next)return;next=t+1000/30;
  const dt=last?Math.min((t-last)/1000,.08):0;last=t;ctx.clearRect(0,0,w,h);
  // Fine stationary beads mixed with larger rivulets, as on a rain-covered window.
  for(const b of beads){ctx.beginPath();ctx.ellipse(b.x,b.y,b.r,b.r*1.18,0,0,Math.PI*2);ctx.fillStyle='rgba(2,12,23,.19)';ctx.fill();ctx.strokeStyle='rgba(198,225,244,.26)';ctx.lineWidth=.45;ctx.stroke();ctx.beginPath();ctx.arc(b.x-b.r*.3,b.y-b.r*.35,Math.max(.2,b.r*.22),0,Math.PI*2);ctx.fillStyle='rgba(235,248,255,.48)';ctx.fill()}
  for(let i=0;i<drops.length;i++){
   const d=drops[i];if(d.wait>0){d.wait-=dt;d.v*=.9}else{d.v=Math.min(d.v+dt*10,7+d.r*d.r*1.0);if(!d.trail.length){for(let k=10;k>0;k--)d.trail.push([d.x+Math.sin(k*.4+d.phase)*.6,d.y-k*(3+d.r*.5)])}d.trail.push([d.x,d.y]);if(d.trail.length>105)d.trail.shift();d.y+=d.v*dt;d.x+=Math.sin(d.y*.026+d.phase)*dt*.8+d.skew*dt;if(random()<dt*.09){d.wait=.6+random()*2.4;d.v*=.15}}
   if(d.y>h+35){drops[i]=drop(true);continue}
   // Nearby beads coalesce, then the heavier drop resumes sliding.
   for(let j=i+1;j<drops.length;j++){const b=drops[j];if(Math.hypot(d.x-b.x,d.y-b.y)<(d.r+b.r)*.62){d.r=Math.min(8.0,Math.sqrt(d.r*d.r+b.r*b.r));d.wait=0;drops[j]=drop(true)}}
   if(d.trail.length>1){const start=d.trail[0],g=ctx.createLinearGradient(start[0],start[1]-1,d.x,d.y+1);g.addColorStop(0,'rgba(185,214,239,0)');g.addColorStop(1,'rgba(185,214,239,.12)');ctx.strokeStyle=g;ctx.lineWidth=Math.max(.6,d.r*.3);ctx.lineCap='round';ctx.beginPath();d.trail.forEach(([x,y],k)=>k?ctx.lineTo(x,y):ctx.moveTo(x,y));ctx.lineTo(d.x,d.y);ctx.stroke()}
   // A dark lens centre, reflected sky crescent and lower caustic suggest clear water.
   outline(d);const lens=ctx.createRadialGradient(d.x-d.r*.35,d.y-d.r*.45,.1,d.x,d.y,d.r*1.35);lens.addColorStop(0,'rgba(219,238,255,.18)');lens.addColorStop(.30,'rgba(164,197,219,.025)');lens.addColorStop(.72,'rgba(1,9,19,.26)');lens.addColorStop(1,'rgba(184,219,246,.18)');ctx.fillStyle=lens;ctx.fill();ctx.strokeStyle='rgba(8,20,33,.35)';ctx.lineWidth=.65;ctx.stroke();
   ctx.beginPath();ctx.ellipse(d.x-d.r*.17,d.y-d.r*.12,d.r*.73,d.r*.88,-.18,Math.PI*1.02,Math.PI*1.65);ctx.strokeStyle='rgba(235,247,255,.63)';ctx.lineWidth=Math.max(.55,d.r*.11);ctx.stroke();
   ctx.beginPath();ctx.ellipse(d.x+d.r*.10,d.y+d.r*.61,d.r*.55,d.r*.20,-.12,0,Math.PI);ctx.strokeStyle='rgba(191,225,252,.42)';ctx.lineWidth=.75;ctx.stroke();
   ctx.beginPath();ctx.ellipse(d.x-d.r*.34,d.y-d.r*.52,Math.max(.35,d.r*.13),d.r*.23,-.4,0,Math.PI*2);ctx.fillStyle='rgba(246,251,255,.8)';ctx.fill();
   ctx.beginPath();ctx.ellipse(d.x+d.r*.40,d.y+d.r*.24,d.r*.15,d.r*.43,.3,0,Math.PI*2);ctx.fillStyle='rgba(202,229,247,.13)';ctx.fill();
  }
 }
 function settings(){if(frame)cancelAnimationFrame(frame);frame=0;last=0;next=0;canvas.hidden=!enabled();if(enabled())frame=requestAnimationFrame(paint);else ctx.clearRect(0,0,w,h)}
 addEventListener('resize',()=>{resize();settings()},{passive:true});document.addEventListener('visibilitychange',settings);reduced.addEventListener('change',settings);new MutationObserver(settings).observe(document.documentElement,{attributes:true,attributeFilter:['class']});resize();settings();
})();
