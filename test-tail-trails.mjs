import assert from 'node:assert/strict';
import {makeRoute,sampleRoute} from './dist/route-state.js';
import {sampleTailTrail} from './dist/tail-trail-state.js';
for(const phone of [false,true]){
 const r=makeRoute(phone);
 for(const p of [0,.01,.2,.5,.8,1]){
  const a=sampleTailTrail(r,p);assert.deepEqual(a,sampleTailTrail(makeRoute(phone),p));
  assert.equal(a.length,45);assert.equal(a.at(-1).fade,0);
  const pose=sampleRoute(r,p),mid=a[0].centres;
  assert.ok(Math.abs(Math.hypot(mid[0][0]-mid[1][0],mid[0][2]-mid[1][2])-1.4*r.scale)<1e-10);
  for(const s of a)assert.ok(s.centres.flat().every(Number.isFinite));
  if(p===0||p===1)assert.ok(a.every(s=>s.fade===0));
 }
 const ps=[.2,.4,.7];assert.deepEqual(ps.map(p=>sampleTailTrail(r,p)),ps.reverse().map(p=>sampleTailTrail(r,p)).reverse());
}
console.log('Passed: trail attachment spacing, desktop/mobile, deterministic stop/reverse/reload, finite geometry, parked fade.');
