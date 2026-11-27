// Dimensions are scene units and the drawings illustrate generic equipment.
export const ink = '#193c36';
const mint = '#b6cab2';
const chalk = '#eee9d8';
const metal = '#739487';
const deep = '#2b554c';
const lime = '#d0ea62';
const copper = '#bf7b45';

type XYZ = [number, number, number];
export const project = ([x, y, z]: XYZ) => [x * .86 - y * .8, x * .36 + y * .4 - z] as const;
const str = (point: XYZ) => project(point).join(',');
const line = (a: XYZ, b: XYZ) => 'M' + str(a) + 'L' + str(b);
const poly = (points: XYZ[]) => points.map(str).join(' ');

type BlockProps = { x?: number; y?: number; z?: number; w: number; l: number; h: number; colors?: [string, string, string]; edge?: string };
export function IsoBlock({x=0,y=0,z=0,w,l,h,colors=[chalk,mint,metal],edge=ink}: BlockProps) {
  return <g stroke={edge} strokeWidth="2.1" strokeLinejoin="round">
    <polygon fill={colors[1]} points={poly([[x,y+l,z],[x+w,y+l,z],[x+w,y+l,z+h],[x,y+l,z+h]])}/>
    <polygon fill={colors[2]} points={poly([[x+w,y,z],[x+w,y+l,z],[x+w,y+l,z+h],[x+w,y,z+h]])}/>
    <polygon fill={colors[0]} points={poly([[x,y,z+h],[x+w,y,z+h],[x+w,y+l,z+h],[x,y+l,z+h]])}/>
  </g>;
}

export function ServerRack({x=0,y=0,t=0,power=1}:{x?:number;y?:number;t?:number;power?:number}) {
  const rackWidth=59, depth=55, height=114;
  return <g>
    <IsoBlock x={x} y={y} w={rackWidth} l={depth} h={height} colors={['#aabdb0','#25463f','#405d54']}/>
    {Array.from({length:10},(_,i)=>{
      const row=100-i*9;
      const [lx,ly]=project([x+47,y+depth+1,row-1]);
      return <g key={i}>
        <path d={line([x+4,y+depth+1,row],[x+52,y+depth+1,row])} stroke={i%3===0?'#b0baa4':'#7d9181'} strokeWidth="3.4"/>
        <circle cx={lx} cy={ly} r="1.9" fill={power>0 && Math.sin(t*2.4+i*1.3) > -.7?lime:deep}/>
      </g>;
    })}
    {[12,17,22,27,32,37,42].map(i=><path key={i} d={line([x+rackWidth,y+i,20],[x+rackWidth,y+i,88])} stroke="#76877a" strokeWidth="1.2"/>)}
  </g>;
}

function Rotor({x,y,z,rad,t}:{x:number;y:number;z:number;rad:number;t:number}){
  const [cx,cy]=project([x,y,z]);
  return <g transform={`translate(${cx} ${cy}) scale(1 .43)`}>
    <circle r={rad} fill={deep} stroke={ink} strokeWidth="3"/>
    <g transform={`rotate(${(t*95)%360})`}>{[0,72,144,216,288].map(a=><path key={a} transform={`rotate(${a})`} d={`M2 0 Q${rad*.45} ${-rad*.75} ${rad*.88} ${-rad*.38} Q${rad*.45} 0 5 4Z`} fill="#c3d2be"/>)}</g>
    <circle r={rad*.22} fill={copper} stroke={ink} strokeWidth="2"/>
    <circle r={rad*.85} fill="none" stroke="#9db0a1" strokeWidth="1"/>
  </g>;
}

export function Chiller({x=0,y=0,z=0,t=0}:{x?:number;y?:number;z?:number;t?:number}){
  return <g>
    <IsoBlock x={x} y={y} z={z} w={135} l={54} h={47} colors={['#e4e7d9','#8ba398','#6c867c']}/>
    <Rotor x={x+35} y={y+28} z={z+48} rad={18} t={t}/>
    <Rotor x={x+101} y={y+28} z={z+48} rad={18} t={t+.9}/>
    {[0,1,2,3,4,5].map(i=><path key={i} stroke={deep} strokeWidth="1.45" d={line([x+7,y+54,z+11+i*5],[x+127,y+54,z+11+i*5])}/>)}
  </g>;
}

export function Transformer({x=0,y=0}:{x?:number;y?:number}) {
  return <g>
    <IsoBlock x={x} y={y} w={87} l={72} h={10} colors={[chalk,metal,deep]}/>
    <IsoBlock x={x+8} y={y+8} z={10} w={70} l={51} h={56} colors={['#ccbc8e','#a6a179','#817b5d']}/>
    {[0,1,2,3,4,5,6,7].map(i=><path key={i} d={line([x+14+i*8,y+60,17],[x+14+i*8,y+60,57])} stroke={deep} strokeWidth="3"/>)}
    {[12,36,61].map((v,i)=>{
      const [cx,cy]=project([x+v,y+28,65]);
      return <g key={v} transform={`translate(${cx} ${cy})`}>
        <path d="M0 0v-31" stroke={copper} strokeWidth="6"/>
        {[0,1,2,3].map(j=><ellipse key={j} cy={-7-j*6} rx={7-j*.7} ry="2.7" fill={i===1?chalk:mint} stroke={ink} strokeWidth="1"/>)}
      </g>;
    })}
  </g>;
}

// Roof moves forward/up as one assembly to expose two server aisles.
export function DataHall({t=0,open=0,powered=true}:{t?:number;open?:number;powered?:boolean}){
  const p = Math.min(1,Math.max(0,open));
  return <g>
    <IsoBlock x={-14} y={-14} w={372} l={216} h={10} colors={['#c8ccb6','#a2ac99','#7a8d7d']}/>
    <IsoBlock x={0} y={0} z={10} w={343} l={183} h={13} colors={['#d7d5bb','#acae95','#788674']}/>
    <IsoBlock x={0} y={0} z={23} w={343} l={5} h={125} colors={['#b0beb0','#9cae9e','#698575']}/>
    <IsoBlock x={0} y={0} z={23} w={4} l={183} h={125} colors={['#b0beb0','#acc2ac','#839d8c']}/>
    <g transform="translate(0 -23)">
      {[13,97].flatMap(y=>[19,98,177,256].map(x=><ServerRack key={x+'-'+y} x={x} y={y} t={t+x/43} power={powered?1:0}/>))}
    </g>
    <g opacity={1-p}>
      <IsoBlock x={0} y={180} z={23} w={343} l={4} h={125} colors={['#d3d5bd','#ced0b8','#667c6c']}/>
      <IsoBlock x={339} y={0} z={23} w={4} l={183} h={125} colors={['#d7d8c2','#b8c3ad','#9eb19d']}/>
      {[0,1,2,3,4,5,6,7,8].map(i=><g key={i}>
        <path d={line([15+i*37,185,25],[15+i*37,185,145])} stroke="#8d9d86" strokeWidth="1.8"/>
        <path d={line([18+i*37,185,113],[44+i*37,185,113])} stroke={deep} strokeWidth="12"/>
        <path d={line([18+i*37,185,108],[44+i*37,185,108])} stroke={metal} strokeWidth="2"/>
      </g>)}
      {[0,1,2,3].map(i=><path key={i} d={line([344,14+i*44,37],[344,14+i*44,135])} stroke={metal} strokeWidth="2"/>)}
      <path d={line([0,185,94],[342,185,94])} stroke={ink} strokeWidth="4"/>
    </g>
    <g opacity={Math.max(0,1-p*.97)} transform={`translate(${p*37} ${-p*126})`}>
      <IsoBlock x={-3} y={-3} z={148} w={350} l={190} h={8} colors={['#e9e7d5','#9cae99','#a4b49f']}/>
      {[1,2,3,4,5,6,7,8].map(i=><path key={i} d={line([i*38,0,156],[i*38,183,156])} stroke="#aeb9a4" strokeWidth="1.4"/>)}
      <Chiller x={21} y={10} z={156} t={t}/>
      <Chiller x={178} y={14} z={156} t={t+.3}/>
      {[0,1].map(i=><path key={i} d={'M'+str([25,90+i*10,158])+'L'+str([310,90+i*10,158])+'L'+str([310,154+i*10,158])} stroke={i?metal:copper} strokeWidth="5" fill="none"/>)}
    </g>
  </g>;
}
