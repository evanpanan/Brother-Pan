import type React from 'react';
export const C={bg:'#f3ede1',ink:'#183e2d',lime:'#c6ec28',sage:'#b9c7a8',pale:'#e1e5d4',gold:'#d4a45c',car:'#cfa55d',red:'#b85c43',white:'#fffaf1',gray:'#8e9c8b'};
export const clamp=(v:number)=>Math.max(0,Math.min(1,v));
export const E=(v:number)=>{v=clamp(v);return v*v*(3-2*v)};
export const V=(t:number,a=0,b=a+1)=>E((t-a)/(b-a));
export const L=(a:number,b:number,q:number)=>a+(b-a)*q;
export const T=({x=540,y,s=36,c=C.ink,anchor='middle',children}:{x?:number,y:number,s?:number,c?:string,anchor?:'middle'|'start'|'end',children:React.ReactNode})=><text data-safe-text="true" x={x} y={y} fontFamily="Head" fontSize={s} fill={c} textAnchor={anchor}>{children}</text>;
export const R=({x,y,w,h,c=C.lime,r=16,stroke='none'}:{x:number,y:number,w:number,h:number,c?:string,r?:number,stroke?:string})=><rect x={x} y={y} width={w} height={h} fill={c} rx={r} stroke={stroke} strokeWidth={4}/>;
