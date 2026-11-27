import type {ReactNode} from 'react';
export const K={paper:'#f5efdf',ink:'#163d33',green:'#365f4e',lime:'#cee849',sage:'#bdcba9',gold:'#d5a45c',copper:'#ac683b',red:'#bd5c42',cream:'#fff9e9',gray:'#778b78',night:'#163b32'};
export const clamp=(v:number)=>Math.max(0,Math.min(1,v));
export const ease=(v:number)=>{const n=clamp(v);return n*n*(3-2*n)};
export const q=(t:number,a:number,b:number)=>ease((t-a)/(b-a));
export const lerp=(a:number,b:number,p:number)=>a+(b-a)*p;
export function settle(t:number){const u=Math.max(0,t);return 1-Math.exp(-u*6)*Math.cos(u*10)}
export function Text({x=540,y,size=40,fill=K.ink,children,anchor='middle',font='Head'}:{x?:number;y:number;size?:number;fill?:string;children:ReactNode;anchor?:'start'|'middle'|'end';font?:string}){
 return <text x={x} y={y} textAnchor={anchor} fill={fill} fontFamily={font} fontSize={size}>{children}</text>;
}
export function Trace({d,t,start=0,duration=1,color=K.ink,width=5}:{d:string;t:number;start?:number;duration?:number;color?:string;width?:number}){
 return <path d={d} pathLength={100} fill="none" stroke={color} strokeWidth={width} strokeLinecap="round" strokeLinejoin="round" strokeDasharray="100" strokeDashoffset={100*(1-q(t,start,start+duration))}/>;
}
export function Coin({x,y,scale=1,rotate=0}:{x:number;y:number;scale?:number;rotate?:number}){
 return <g transform={`translate(${x} ${y}) rotate(${rotate}) scale(${scale})`}><ellipse cy="5" rx="38" ry="34" fill="#a46a35"/><circle r="35" fill={K.gold} stroke={K.ink} strokeWidth="3"/><circle r="27" fill="none" stroke="#ffe2a7" strokeWidth="2"/><rect x="-8" y="-8" width="16" height="16" rx="3" fill={K.ink}/><path d="M-19-19q19-14 38 0" fill="none" stroke="#ffedbc" strokeWidth="3"/></g>;
}
export function Packet({x,y,rotate=0,scale=1,label='资金'}:{x:number;y:number;rotate?:number;scale?:number;label?:string}){
 return <g transform={`translate(${x} ${y}) rotate(${rotate}) scale(${scale})`}><path d="M-87-46H87V46H-87Z" fill={K.cream} stroke={K.ink} strokeWidth="3"/><path d="M-87-46 0 9 87-46M-87 46l57-52M87 46 30-6" fill="none" stroke={K.copper} strokeWidth="2"/><Text x={0} y={31} size={23}>{label}</Text></g>;
}
export function Hand({x,y,angle=0,scale=1,open=false}:{x:number;y:number;angle?:number;scale?:number;open?:boolean}){
 return <g transform={`translate(${x} ${y}) rotate(${angle}) scale(${scale})`} stroke={K.ink} strokeWidth="3" strokeLinejoin="round">
 <path d="M-135 10H-53V67H-135Z" fill="#b6cbd0"/><path d="M-62 9h20v61h-20Z" fill={K.cream}/>
 <path d={open?"M-40 16-17-5q14-16 24-5 5 7-5 20L18-3q12-12 20-2 6 8-4 17l-7 7 24-10q14-6 18 6 3 9-9 15L39 40l24-2q15-1 15 11 0 9-15 11l-32 5q-35 17-72-2Z":"M-40 17-4 1q17-10 27-1l27 25q12 12 1 20-7 5-17-4L15 27l-2 10 22 15q13 11 3 20-7 5-17-1L6 62q-21 18-46 0Z"} fill="#f0c68e"/>
 <path d="M-26 21q15 9 21 26" fill="none" stroke="#b17e52" strokeWidth="2"/></g>;
}
export function Rack({x,y,t=0,scale=1,open=0,lit=1}:{x:number;y:number;t?:number;scale?:number;open?:number;lit?:number}){
 return <g transform={`translate(${x} ${y}) scale(${scale})`}>
 <ellipse cy="232" rx="102" ry="20" fill={K.ink} opacity=".12"/>
 <path d="M-76-158 57-188 99-166-33-134Z" fill="#72917e" stroke={K.ink} strokeWidth="3"/>
 <path d="M57-188 99-166V214l-42 22Z" fill="#608471" stroke={K.ink} strokeWidth="3"/>
 <rect x="-76" y="-158" width="133" height="394" rx="7" fill="#294e40" stroke={K.ink} strokeWidth="4"/>
 {Array.from({length:8},(_,i)=><g key={i}><rect x="-63" y={-138+i*44} width="105" height="33" rx="3" fill="#819783" stroke={K.ink} strokeWidth="2"/><path d={`M-53 ${-124+i*44}h47m-47 7h35`} stroke="#3d6251" strokeWidth="3"/><circle cx="25" cy={-121+i*44} r="4" fill={lit&&Math.sin(t*4+i)>.0?K.lime:'#496550'}/></g>)}
 <g transform={`translate(-76 -158) skewY(${-10*open}) scale(${1-open*.78} 1)`} opacity={1-open*.83}><rect width="133" height="394" rx="6" fill="#24493c" stroke="#849981" strokeWidth="4"/>{Array.from({length:16},(_,i)=><path key={i} d={`M12 ${14+i*23}h109`} stroke="#607f69" strokeWidth="2"/>)}<rect x="112" y="178" width="6" height="33" rx="3" fill={K.gold}/></g>
 </g>;
}
export function Chip({x,y,t=0,scale=1,tilt=0,label='GPU'}:{x:number;y:number;t?:number;scale?:number;tilt?:number;label?:string}){
 return <g transform={`translate(${x} ${y}) rotate(${tilt}) scale(${scale})`} stroke={K.ink}>
 <ellipse cy="97" rx="117" ry="17" fill={K.ink} opacity=".13"/>
 {Array.from({length:10},(_,i)=><path key={i} d={`M${-72+i*16}-87v-18M${-72+i*16} 87v18M-87 ${-72+i*16}h-18M87 ${-72+i*16}h18`} stroke={K.gold} strokeWidth="6"/>)}
 <rect x="-87" y="-87" width="174" height="174" rx="10" fill={K.green} strokeWidth="4"/><rect x="-65" y="-65" width="130" height="130" rx="4" fill={K.lime} strokeWidth="2"/>
 {Array.from({length:8},(_,i)=><path key={i} d={`M-57 ${-49+i*14}h${25+(i*19)%84}`} stroke="#68823b" opacity=".36" strokeWidth="3"/>)}
 <Text x={0} y={12} size={32}>{label}</Text><circle cx="-77" cy="-77" r="4" fill={K.cream}/></g>;
}
export function Tower({x,y,scale=1}:{x:number;y:number;scale?:number}){
 return <g transform={`translate(${x} ${y}) scale(${scale})`} stroke={K.ink} fill="none" strokeWidth="4" strokeLinejoin="round"><path d="M-66 210 0-84 66 210M-32 68 32 133-47 133 47 68ZM-48 132 53 194H-61L43 133M-78-31H78M-99 6H99M-25-57H25M-44 41H44M-16-84 0-101 16-84"/><path d="M-86-30v20m172-20v20M-100 7v18m200-18v18" strokeWidth="7"/></g>;
}
export function Building({x,y,scale=1,t=0,build=1,label='机房'}:{x:number;y:number;scale?:number;t?:number;build?:number;label?:string}){
 return <g transform={`translate(${x} ${y}) scale(${scale})`}>
 <ellipse cy="151" rx="230" ry="28" fill={K.ink} opacity=".12"/>
 <g opacity={build} transform={`translate(0 ${(1-build)*94})`}>
 <path d="M-211-58 81-139 222-62-64 26Z" fill="#d7dcc3" stroke={K.ink} strokeWidth="4"/>
 <path d="M-211-58-64 26V150l-147-77Z" fill="#b5c2a4" stroke={K.ink} strokeWidth="4"/>
 <path d="M-64 26 222-62V66L-64 150Z" fill="#809b7f" stroke={K.ink} strokeWidth="4"/>
 {Array.from({length:9},(_,i)=><g key={i}><path d={`M${-48+i*30} ${26-i*9.2}v112`} stroke="#4c7058" strokeWidth="3"/>{[0,1,2].map(j=><path key={j} d={`M${-37+i*30} ${39+j*27-i*9.2}l15-5v13l-15 5Z`} fill={Math.sin(t*2+i+j)>.3?K.lime:'#becba5'} stroke="none"/>)}</g>)}
 <g transform="translate(-26 -48) rotate(-15)"><rect x="-116" y="-29" width="219" height="56" rx="5" fill={K.cream} stroke={K.ink} strokeWidth="2"/><Text x={-6} y={8} size={27}>{label}</Text></g>
 </g></g>;
}
export function Truck({x,y,scale=1,load=true,t=0}:{x:number;y:number;scale?:number;load?:boolean;t?:number}){
 return <g transform={`translate(${x} ${y}) scale(${scale})`} stroke={K.ink} strokeWidth="3">
 <ellipse cy="69" rx="157" ry="13" fill={K.ink} opacity=".13"/><path d="M-150 16H47v36h-197Z" fill={K.gold}/><path d="M45-43h59l42 58v37H45Z" fill={K.sage}/><path d="M62-30h33l29 43H62Z" fill="#f5efdf"/>
 {load&&<g transform="translate(-48 -81) scale(.42)"><Rack x={0} y={0} open={.2} t={t}/></g>}
 {[-100,92].map(x=><g key={x} transform={`translate(${x} 48) rotate(${t*190})`}><circle r="26" fill={K.ink}/><circle r="13" fill={K.gold}/><path d="M-13 0h26M0-13v26" stroke={K.cream}/></g>)}</g>;
}
export function Pen({x,y,angle=0,scale=1}:{x:number;y:number;angle?:number;scale?:number}){
 return <g transform={`translate(${x} ${y}) rotate(${angle}) scale(${scale})`} stroke={K.ink} strokeWidth="3"><path d="M0 0 10-35 20-35 28-11Z" fill="#d5ac71"/><path d="M0 0 9-13 14-7Z" fill={K.ink}/><path d="M10-35 143-199l20 17L28-11Z" fill={K.gold}/><path d="M15-30 147-193" stroke={K.cream} strokeWidth="3"/><path d="M143-199 151-210q5-7 12-2l8 7q5 5 1 12l-9 11Z" fill={K.red}/></g>;
}
export function Skyline({t=0,dark=false}:{t?:number;dark?:boolean}){
 const c=dark?'#4b7058':'#cbd5b9';
 return <g opacity=".55">{Array.from({length:13},(_,i)=><g key={i} transform={`translate(${i*110-105-t*3} ${1100+(i%3)*15})`}><path d={`M0 0v${-80-(i%5)*39}h76V0Z`} fill={c}/><path d={`M-10 0H87`} stroke={c} strokeWidth="4"/></g>)}<path d="M0 1130Q250 1095 540 1130T1080 1120V1260H0Z" fill={dark?'#315742':'#d7dfc4'}/></g>;
}
