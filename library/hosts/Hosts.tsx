import mouths from './pose-mouths.json';
import {staticFile,delayRender,continueRender,cancelRender} from 'remotion';
import {useEffect,useLayoutEffect,useRef,useState} from 'react';
type P={x:number,y:number};
const ease=(v:number)=>{const a=Math.max(0,Math.min(1,v));return a*a*(3-2*a)};
const pulse=(t:number,a:number,b:number,c:number,d:number)=>ease((t-a)/(b-a))*(1-ease((t-c)/(d-c)));
function triangle(c:CanvasRenderingContext2D,im:HTMLCanvasElement,s:P[],v:P[]){
 const [a,b,d]=s,[u,w,z]=v,det=(b.x-a.x)*(d.y-a.y)-(b.y-a.y)*(d.x-a.x);
 const A=((w.x-u.x)*(d.y-a.y)-(z.x-u.x)*(b.y-a.y))/det,B=((w.y-u.y)*(d.y-a.y)-(z.y-u.y)*(b.y-a.y))/det,C=((z.x-u.x)*(b.x-a.x)-(w.x-u.x)*(d.x-a.x))/det,D=((z.y-u.y)*(b.x-a.x)-(w.y-u.y)*(d.x-a.x))/det,E=u.x-A*a.x-C*a.y,F=u.y-B*a.x-D*a.y;
 c.save();const mx=(u.x+w.x+z.x)/3,my=(u.y+w.y+z.y)/3;c.beginPath();[u,w,z].forEach((q,i)=>{const dx=q.x-mx,dy=q.y-my,l=Math.hypot(dx,dy)||1,x=q.x+dx/l*.65,y=q.y+dy/l*.65;i?c.lineTo(x,y):c.moveTo(x,y)});c.closePath();c.clip();c.setTransform(A,B,C,D,E,F);c.drawImage(im,0,0);c.restore();
}
function Puppet({name,t,talking,pose}:{name:'pan'|'chili',t:number,talking:boolean,pose:number}){
 const ref=useRef<HTMLCanvasElement>(null),layer=useRef<HTMLCanvasElement|null>(null),ready=useRef(false),[image,setImage]=useState<HTMLImageElement|null>(null),[handle]=useState(()=>delayRender('Loading approved character artwork'));
 useEffect(()=>{const im=new Image();im.onload=()=>setImage(im);im.onerror=()=>cancelRender(new Error('Character artwork missing'));im.src=staticFile('host-poses.png');},[name]);
 useLayoutEffect(()=>{if(!image||!ref.current)return;const cv=ref.current,c=cv.getContext('2d')!;if(!layer.current)layer.current=document.createElement('canvas');const src=layer.current;src.width=1280;src.height=1280;const p=src.getContext('2d')!;const pan=name==='pan',col=Math.max(0,Math.min(3,pose)),cw=image.width/4,ch=image.height/2; p.drawImage(image,col*cw,pan?0:ch,cw,ch,0,0,1280,1280);const mouth=mouths[pan?0:1][col];
 if(talking){const h=10+Math.abs(Math.sin(t*10.3))*24,w=mouth.w;p.save();p.translate(mouth.x,mouth.y+3);p.rotate(0);p.fillStyle='#953e25';p.strokeStyle='#85371f';p.lineWidth=6;p.beginPath();p.moveTo(-w/2,0);p.quadraticCurveTo(0,20,w/2,0);p.quadraticCurveTo(w*.38,15+h,0,20+h);p.quadraticCurveTo(-w*.35,18+h,-w/2,0);p.fill();p.stroke();p.fillStyle='#ee7850';p.beginPath();p.moveTo(-w*.26,20+h*.7);p.quadraticCurveTo(0,12+h*.65,w*.26,20+h*.7);p.quadraticCurveTo(0,29+h*.7,-w*.26,20+h*.7);p.fill();p.restore();}
 const emph=talking?pulse(t,.35,.95,1.7,2.7)+.7*pulse(t,5.2,6.1,6.8,7.8)+.55*pulse(t,11,12,13,14):0;
 const nod=talking?pulse(t,3,3.5,3.8,4.4):pulse(t,1.3,1.7,2,2.6),lean=(talking?1.8*emph:.5*nod)*(pan?1:-1)*Math.PI/180,head=(-1.6*emph+1.8*nod)*(pan?1:-1)*Math.PI/180;
 const warp=(x:number,y:number):P=>{let X=x,Y=y;const hw=1-ease((y-580)/170),ha=head*hw,dx=x-650,dy=y-670;X=650+dx*Math.cos(ha)-dy*Math.sin(ha);Y=670+dx*Math.sin(ha)+dy*Math.cos(ha);const wx=(pan?[330,1000,800,1000]:[320,1000,450,1000])[col],wy=(pan?[700,900,950,800]:[720,1050,700,780])[col],aw=Math.exp(-(((x-wx)/245)**2)-((y-wy)/240)**2)*ease((y-570)/100)*(pan?1:1-ease((x-440)/180));X+=(pan?45:-35)*emph*aw;Y-=(pan?75:70)*emph*aw;const lower=Math.exp(-(((x-650)/260)**2)-((y-1160)/150)**2);X+=(pan?15:-18)*emph*lower;const bx=X-650,by=Y-1210;return{x:650+bx*Math.cos(lean)-by*Math.sin(lean),y:1210+bx*Math.sin(lean)+by*Math.cos(lean)}};
 c.clearRect(0,0,1280,1280);const xs=[0,160,300,430,560,690,820,950,1080,1280],ys=[0,160,300,440,580,700,820,940,1060,1170,1280];for(let j=0;j<ys.length-1;j++)for(let i=0;i<xs.length-1;i++){const a={x:xs[i],y:ys[j]},b={x:xs[i+1],y:ys[j]},d={x:xs[i],y:ys[j+1]},e={x:xs[i+1],y:ys[j+1]};triangle(c,src,[a,b,e],[warp(a.x,a.y),warp(b.x,b.y),warp(e.x,e.y)]);triangle(c,src,[a,e,d],[warp(a.x,a.y),warp(e.x,e.y),warp(d.x,d.y)])}if(!ready.current){ready.current=true;continueRender(handle)}
 },[image,t,talking,name,pose,handle]);
 return <foreignObject x={-55} y={25} width="480" height="480"><canvas ref={ref} width={1280} height={1280} style={{width:480,height:480}}/></foreignObject>;
}
export const Pan=({t,talking=false,pose=0}:{t:number,talking?:boolean,pose?:number})=><Puppet name="pan" t={t} talking={talking} pose={pose}/>;
export const Chili=({t,talking=false,pose=0}:{t:number,talking?:boolean,pose?:number})=><Puppet name="chili" t={t} talking={talking} pose={pose}/>;
