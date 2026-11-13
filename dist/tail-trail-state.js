import {sampleRoute,clamp} from './route-state.js';
// Tail-lamp ribbons are sampled by route distance, never elapsed time.
export function sampleTailTrail(route,progress,segments=44,direction=1){
 const p=clamp(progress),length=Math.min(route.scale*4.6,(direction<0?1-p:p)*route.length),parking=clamp((1-p)/.022)*clamp(p/.012),samples=[];
 for(let i=0;i<=segments;i++){
  const t=i/segments,q=clamp(p-direction*length*t/route.length),pose=sampleRoute(route,q),c=Math.cos(pose.heading+(direction<0?Math.PI:0)),s=Math.sin(pose.heading+(direction<0?Math.PI:0));
  samples.push({centres:[-.7,.7].map(x=>[pose.position[0]+route.scale*(c*x-s*2.29),.626*route.scale,pose.position[2]+route.scale*(-s*x-c*2.29)]),normal:[c,0,-s],fade:Math.pow(1-t,1.8)*parking});
 }
 return samples;
}
