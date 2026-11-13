import {CatmullRomCurve3,Vector3} from './vendor/three.module.js';
export const WHEEL_RADIUS=.355,WHEELBASE=2.76;
export const clamp=(v,a=0,b=1)=>Math.max(a,Math.min(b,v));
export function makeRoute(narrow=false,aspect=16/9){
 const points=narrow?[[1.35,0,3.7],[.7,0,4.1],[-1.15,0,4.6],[-1.45,0,4.1],[1.25,0,3.8],[1.4,0,4.5],[-1.2,0,4.4],[-1.3,0,3.9],[1.3,0,4],[1.35,0,4.15]]:[[4.2,0,3.6],[2.8,0,4.1],[-3.7,0,4.8],[-4.3,0,4.1],[3.8,0,3.5],[4.2,0,4.5],[-3.6,0,4.7],[-4.1,0,3.9],[3.8,0,3.8],[4.2,0,4.1]];
 const curve=new CatmullRomCurve3(points.map(p=>new Vector3(p[0]*(narrow?.72:Math.min(1,aspect/1.5)),p[1],p[2])),false,'centripetal');curve.arcLengthDivisions=4096;curve.updateArcLengths();
 return {curve,length:curve.getLength(),scale:narrow?.29:.43};
}
export function sampleRoute(route,progress){
 const p=clamp(progress),s=p*route.length,position=route.curve.getPointAt(p),tangent=route.curve.getTangentAt(p).normalize(),e=.001;
 const a=route.curve.getTangentAt(clamp(p-e)),b=route.curve.getTangentAt(clamp(p+e));
 const delta=Math.atan2(a.z*b.x-a.x*b.z,a.x*b.x+a.z*b.z),ds=(clamp(p+e)-clamp(p-e))*route.length,curvature=ds>0?delta/ds:0;
 const park=clamp((1-p)/.035)*clamp(p/.02);
 return {p,distance:s,position:position.toArray(),heading:Math.atan2(tangent.x,tangent.z),wheel:s/(WHEEL_RADIUS*route.scale),steering:clamp(Math.atan(WHEELBASE*route.scale*curvature),-.36,.36)*park,lean:clamp(-curvature*.022,-.025,.025)*park,scale:route.scale};
}
export function pageProgress(y,height,viewport){return clamp(y/Math.max(1,height-viewport));}


