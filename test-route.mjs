import assert from 'node:assert/strict';
import {makeRoute,sampleRoute,WHEEL_RADIUS,pageProgress} from './dist/route-state.js';
const results=[];
for(const phone of [false,true]){
 const r=makeRoute(phone),samples=[0,.1,.25,.5,.73,.9,1];
 const forward=samples.map(p=>sampleRoute(r,p));
 const reverse=[...samples].reverse().map(p=>sampleRoute(r,p)).reverse();
 assert.deepEqual(forward,reverse);
 for(const pose of forward){assert.ok(Math.abs(pose.wheel*WHEEL_RADIUS*r.scale-pose.distance)<1e-10);assert.deepEqual(pose,sampleRoute(makeRoute(phone),pose.p));}
 const stopped=sampleRoute(r,.413);for(let i=0;i<200;i++)assert.deepEqual(stopped,sampleRoute(r,.413));
 // Equal progress steps should have near-equal travelled chord lengths.
 const d=[];for(let i=1;i<=1000;i++){const a=r.curve.getPointAt((i-1)/1000),b=r.curve.getPointAt(i/1000);d.push(a.distanceTo(b));}
 const ratio=Math.max(...d)/Math.min(...d);assert.ok(ratio<1.15,`arc-length variation ${ratio}`);
 assert.ok(Math.abs(sampleRoute(r,1).steering)<1e-12);assert.ok(Math.abs(sampleRoute(r,1).lean)<1e-12);
 results.push({phone,routeLength:r.length,equalStepRatio:ratio,deterministic:true,wheelDistanceExact:true});
}
assert.equal(pageProgress(500,2000,1000),.5);
console.log(JSON.stringify({passed:true,checks:['forward/reverse equality','reconstruction at same progress','stop stability','distance/radius wheels','arc-length consistency','parked pose'],results},null,2));

