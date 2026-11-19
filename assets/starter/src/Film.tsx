import {useCurrentFrame,staticFile} from 'remotion';
import {Audio} from '@remotion/media';
import data from './episode.json';
import {Stage} from './library/Stage';
import {Host} from './library/hosts/Host';
import {C,T,R,V} from './library/theme';
import {Chip} from './library/vector/chips';
import {Rocket} from './library/vector/space';
import {MonthlyCost,GeofenceDiagram,LicenseGates,ArrayGrid,IncomeFlow} from './library/scenes/Mechanisms';
type Gaze='viewer'|'partner'|'subject';
type PoseCue={at:number;pose:number;gaze?:Gaze};
type Visual={pan?:PoseCue[];chili?:PoseCue[];price?:number;monthly?:number;freeMonths?:number};
type Shot={sceneId:string;kind:string;speaker:'M'|'F';text:string;start:number;frames:number;caps:{text:string;startMs:number;endMs:number}[];visual?:Visual};
type Episode={title:string;brand:string;fps:number;audio?:string;scenes:Shot[]};
const episode=data as unknown as Episode;
function poseAt(cues:PoseCue[]|undefined,t:number,fallback:PoseCue){return cues?.filter(c=>c.at<=t).at(-1)||fallback;}
export const Film=()=>{
 const f=useCurrentFrame(),shot=episode.scenes.find(s=>f>=s.start&&f<s.start+s.frames)||episode.scenes.at(-1)!,t=(f-shot.start)/episode.fps,cap=shot.caps.find(c=>t*1000>=c.startMs&&t*1000<c.endMs),voicing=!!cap,v=shot.visual||{};
 const pan=poseAt(v.pan,t,{at:0,pose:2,gaze:'viewer'}),chili=poseAt(v.chili,t,{at:0,pose:2,gaze:'partner'});
 let art;
 switch(shot.kind){
 case 'hook':art=<><R x={130} y={920} w={820} h={245} c={C.sage} r={45}/><Host x={120} y={540} scale={.9} t={t} speaker="M" activeSpeaker={shot.speaker} voicing={voicing} pose={pan.pose} gaze={pan.gaze}/><Host x={575} y={540} scale={.9} t={t} speaker="F" activeSpeaker={shot.speaker} voicing={voicing} pose={chili.pose} gaze={chili.gaze}/><g opacity={1-V(t,.8,1.5)}><R x={175} y={1030} w={730} h={205} c={C.ink}/><T y={1110} s={70} c={C.white}>人物不用重画</T><T y={1195} s={72} c={C.lime}>新故事照样演？</T></g></>;break;
 case 'chip':art=<><Chip x={540} y={830} z={1.25} open={V(t,.2,1.8)*1.8}/><T y={1200} s={26}>功能展开示意 · 不是实际封装剖面</T></>;break;
 case 'array':art=<ArrayGrid t={t}/>;break;
 case 'geofence':art=<GeofenceDiagram t={t}/>;break;
 case 'cost':art=<MonthlyCost t={t} price={v.price??20000} monthly={v.monthly??100} freeMonths={v.freeMonths??1}/>;break;
 case 'gates':art=<LicenseGates t={t}/>;break;
 case 'income':art=<IncomeFlow t={t}/>;break;
 case 'rocket':art=<><Rocket x={540} y={1100-100*V(t,.5,3)} flame={40+20*Math.sin(t*5)} z={1.5}/><T y={1210} s={24}>飞行动作示意 · 非工程比例</T></>;break;
 case 'intro':case 'duo':case 'outro':art=<><R x={130} y={920} w={820} h={245} c={C.sage} r={45}/><Host x={140} y={575} scale={.86} t={t} speaker="M" activeSpeaker={shot.speaker} voicing={voicing} pose={pan.pose} gaze={pan.gaze}/><Host x={550} y={575} scale={.86} t={t} speaker="F" activeSpeaker={shot.speaker} voicing={voicing} pose={chili.pose} gaze={chili.gaze}/>{shot.kind==='outro'&&<><R x={230} y={1140} w={620} h={90} c={C.ink}/><T y={1202} s={42} c={C.lime}>关注华尔街潘哥</T></>}</>;break;
 default:throw new Error(`Scene kind '${shot.kind}' has no renderer. Design and implement this scene in Film.tsx before export.`);
 }
 return <><Stage title={episode.title} brand={episode.brand} caption={cap?.text||''}>{art}</Stage>{episode.audio&&<Audio src={staticFile(episode.audio)}/>}</>;
};
