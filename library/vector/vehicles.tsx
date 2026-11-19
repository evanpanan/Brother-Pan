import type React from 'react';
import {C,R} from '../theme';
export function Car({x=0,y=0,z=1,t=0,open=0}:{x?:number,y?:number,z?:number,t?:number,open?:number}){return <g transform={`translate(${x} ${y}) scale(${z})`}>
 <ellipse cx="0" cy="99" rx="240" ry="23" fill={C.ink} opacity=".12"/>
 <path d="M-246 20-215-28-120-48-62-107Q30-132 114-89L183-41 246-14 253 54Q245 76 206 78H-204Q-245 73-246 20Z" fill={C.car} stroke={C.ink} strokeWidth="6"/>
 <path d="M-105-48-55-96Q38-115 108-77L151-43Z" fill="#43534a" stroke={C.ink} strokeWidth="4"/><path d="M32-108 45-46" stroke={C.car} strokeWidth="8"/>
 <path d="M-239 24H240M-195 52H195" stroke={C.ink} strokeWidth="3" opacity=".5"/>
 <path d="M-243 13h44M211-8l30 10" stroke={C.white} strokeWidth="9"/>
 {[-161,166].map(x=><g key={x} transform={`translate(${x} 65)`}><circle r="49" fill={C.ink}/><circle r="36" fill={C.gold} stroke={C.car} strokeWidth="5"/><g transform={`rotate(${t*85})`}><circle cx="16" r="3" fill="#b68b45"/><circle cx="-16" r="3" fill="#b68b45"/></g></g>)}
 <path d="M-94-43H111L127 52H-86Z" fill="none" stroke={C.ink} strokeWidth="3"/>
 {open>0&&<g transform={`translate(-84 -44) rotate(${-65*open})`}><path d="M0 0h190l-38-56-90-1Z" fill={C.car} stroke={C.ink} strokeWidth="5"/></g>}
 </g>}

export function Phone({x,y,z=1,children}:{x:number,y:number,z?:number,children?:React.ReactNode}){return <g transform={`translate(${x} ${y}) scale(${z})`}><R x={-125} y={-215} w={250} h={430} c={C.ink} r={32}/><R x={-112} y={-192} w={224} h={380} c={C.white} r={18}/><path d="M-35-200h70M-35 201h70" stroke={C.sage} strokeWidth="5"/>{children}</g>}

export function Steering({x,y,z=1,c=C.ink}:{x:number,y:number,z?:number,c?:string}){return <g transform={`translate(${x} ${y}) scale(${z})`}><circle r="70" stroke={c} strokeWidth="13" fill="none"/><circle r="20" fill={c}/><path d="M0 20v50M-18-4-65-24M18-4 65-24" stroke={c} strokeWidth="12"/></g>}

export function Road({y=1040}:{y?:number}){return <><path d={`M0 ${y}H1080v160H0Z`} fill={C.pale}/><path d={`M0 ${y+80}H1080`} stroke={C.white} strokeWidth="8" strokeDasharray="70 45"/></>}

export function Home({x,y,z=1,office=false}:{x:number,y:number,z?:number,office?:boolean}){return <g transform={`translate(${x} ${y}) scale(${z})`}>{office?<><R x={-70} y={-130} w={140} h={170} c={C.white} stroke={C.ink} r={3}/>{Array.from({length:9},(_,i)=><rect key={i} x={-48+i%3*37} y={-106+Math.floor(i/3)*40} width="22" height="25" fill={C.sage}/>)}<rect x="-17" y="5" width="34" height="35" fill={C.ink}/></>:<><path d="M-80-25 0-100 80-25V55H-80Z" fill={C.gold} stroke={C.ink} strokeWidth="5"/><path d="M-96-20 0-112 96-20" fill="none" stroke={C.ink} strokeWidth="7"/><rect x="-20" width="40" height="55" fill={C.ink}/><rect x="-60" y="-12" width="25" height="26" fill={C.white}/></>}</g>}

export function Icon({x,y,kind,z=1}:{x:number,y:number,kind:number,z?:number}){return <g transform={`translate(${x} ${y}) scale(${z})`}>
 {kind===0?<><circle r="46" fill="none" stroke={C.ink} strokeWidth="6"/><path d="M-28 15-10-15 8 5 27-23" stroke={C.ink} strokeWidth="6" fill="none"/><circle cx="27" cy="-23" r="7" fill={C.gold}/></>:kind===1?<><path d="M-40-10q40-40 80 0M-25 8q25-25 50 0M-10 25q10-10 20 0" stroke={C.ink} strokeWidth="7" fill="none"/><circle cy="39" r="6" fill={C.ink}/></>:kind===2?<><path d="M-43 15v-20a43 43 0 0 1 86 0v20" fill="none" stroke={C.ink} strokeWidth="7"/><R x={-50} y={0} w={20} h={40} c={C.ink} r={5}/><R x={30} y={0} w={20} h={40} c={C.ink} r={5}/><path d="M40 40q0 20-35 20" stroke={C.ink} strokeWidth="5" fill="none"/></>:<><circle r="44" fill="none" stroke={C.ink} strokeWidth="15"/><circle r="20" fill="none" stroke={C.gold} strokeWidth="6"/><path d="M-10-43v20M-10 23v20M-43-10h20M23-10h20" stroke={C.sage} strokeWidth="5"/></>}
 </g>}
