import {C,T} from '../theme';
export function Chip({x=0,y=0,z=1,label='TPU',open=0}:{x?:number,y?:number,z?:number,label?:string,open?:number}){
 return <g transform={`translate(${x} ${y}) scale(${z})`}>
  <ellipse cx="0" cy="140" rx="195" ry="30" fill={C.ink} opacity=".1"/>
  <g transform={`translate(0 ${open*55})`}><path d="M-200-110H200V110H-200Z" fill="#537653" stroke={C.ink} strokeWidth="7"/>
  {Array.from({length:14},(_,i)=><path key={i} d={`M${-165+i*25} 110v25`} stroke={C.gold} strokeWidth="12"/>)}
  {[-1,1].map(a=><g key={a}>{[0,1,2,3].map(i=><g key={i}><rect x={a<0?-178:120} y={-85+i*46} width="58" height="29" rx="3" fill={C.ink}/><path d={`M${a*120} ${-70+i*46}H${a*75}`} stroke={C.sage} strokeWidth="3"/></g>)}</g>)}
  {[[-180,-92],[180,-92],[-180,92],[180,92]].map(([a,b],i)=><circle key={i} cx={a} cy={b} r="9" fill={C.gold}/>)}</g>
  <g transform={`translate(0 ${-open*75})`}><rect x="-92" y="-92" width="184" height="184" rx="11" fill={C.gold} stroke={C.ink} strokeWidth="5"/>
  <rect x="-70" y="-70" width="140" height="140" rx="6" fill={C.ink}/><path d="M-60-60H60V60H-60Z" fill="none" stroke={C.sage} strokeWidth="2"/>
  <T x={0} y={14} s={42} c={C.white}>{label}</T></g>
 </g>;
}

export function TaskIcon({kind,x,y,t}:{kind:number,x:number,y:number,t:number}){return <g transform={`translate(${x} ${y})`}>
 <circle r="78" fill={C.white} stroke={C.sage} strokeWidth="3"/>
 {kind===0?<g transform={`rotate(${t*14})`}><path d="M-38-24 0-45 40-23 40 25 0 47-38 24Z" fill={C.sage} stroke={C.ink} strokeWidth="4"/><path d="M-38-24 0 0 40-23M0 0v47" stroke={C.ink} strokeWidth="4" fill="none"/></g>:kind===1?<g transform={`rotate(${t*10})`}>{[0,60,120].map(a=><ellipse key={a} rx="48" ry="18" transform={`rotate(${a})`} stroke={C.ink} fill="none" strokeWidth="3"/>)}<circle r="8" fill={C.gold}/></g>:<g>{[[0,-32],[-36,20],[36,20]].map(([a,b],i)=><g key={i}><path d={`M${a} ${b}L0 0`} stroke={C.ink} strokeWidth="3"/><circle cx={a} cy={b} r="12" fill={C.lime} stroke={C.ink} strokeWidth="3"/></g>)}<circle r="14" fill={C.ink}/></g>}
 </g>}
