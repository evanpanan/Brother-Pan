import {C,T,V,L} from '../theme';
export type Point={x:number;y:number;label:string;detail?:string};
/** Selected historical nodes or explicitly hypothetical geometry, never a daily price series. */
export function ReboundPath({points,t,seconds=7}:{points:Point[];t:number;seconds?:number}){
 if(points.length<2||seconds<=0||!Number.isFinite(seconds)||!points.every(p=>Number.isFinite(p.x)&&Number.isFinite(p.y)))throw new Error('At least two finite nodes and positive duration required');
 const q=V(t,.3,seconds),pos=q*(points.length-1),k=Math.min(points.length-2,Math.floor(pos)),w=pos-k,a=points[k],b=points[k+1];
 return <g><path d="M150 510V1150H920" stroke={C.sage} strokeWidth={4} fill="none"/>{points.slice(1).map((p,i)=>{const start=points[i],f=Math.max(0,Math.min(1,pos-i));return <path key={i} d={`M${start.x} ${start.y}L${L(start.x,p.x,f)} ${L(start.y,p.y,f)}`} stroke={p.y>start.y?C.red:C.ink} strokeWidth={11} strokeLinecap="round" fill="none"/>})}{points.map((p,i)=>{const below=i===0?points[1].y<p.y:p.y>points[i-1].y,anchor=p.x>760?'end':p.x<300?'start':'middle';return <g key={i} opacity={i===0?1:V(pos,i-.3,i)}><circle cx={p.x} cy={p.y} r={13} fill={C.gold}/><T x={p.x} y={p.y+(below?60:-48)} anchor={anchor} s={30}>{p.label}</T>{p.detail&&<T x={p.x} y={p.y+(below?105:-100)} anchor={anchor} s={27}>{p.detail}</T>}</g>})}<circle cx={L(a.x,b.x,w)} cy={L(a.y,b.y,w)} r={19} fill={C.lime} stroke={C.ink} strokeWidth={3}/></g>;
}
