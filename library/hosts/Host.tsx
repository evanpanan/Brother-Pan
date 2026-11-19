import {Pan,Chili} from './Hosts';
import {FrontPan,FrontChili} from './FrontHosts';
export type Speaker='M'|'F';
export function Host({speaker,activeSpeaker,t,pose=0,gaze='partner',x,y,scale=1,voicing=false}:{speaker:Speaker;activeSpeaker?:Speaker;t:number;pose?:number;gaze?:'viewer'|'partner'|'subject';x:number;y:number;scale?:number;voicing?:boolean}){
 const girl=speaker==='F',front=gaze==='viewer',Person=front?(girl?FrontChili:FrontPan):(girl?Chili:Pan);
 return <g data-character={speaker} data-speaking={voicing&&speaker===activeSpeaker} transform={`translate(${x} ${y}) scale(${scale})`}><Person t={Math.max(0,t)} pose={pose} talking={voicing&&speaker===activeSpeaker}/></g>;
}
