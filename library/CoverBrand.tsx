import {useId} from 'react';
import {staticFile} from 'remotion';

/** Cover top area: avatar, then account name. Topic/title belongs to the main art. */
export function CoverBrand({account='华尔街潘哥',avatar='pan-avatar.png',x=540,top=140,size=136,nameY=334,ink='#183e2d'}:{account?:string;avatar?:string;x?:number;top?:number;size?:number;nameY?:number;ink?:string}){
 const id=`cover-avatar-${useId().replace(/:/g,'')}`;
 return <g data-role="cover-brand"><defs><clipPath id={id}><circle cx={x} cy={top+size/2} r={size/2}/></clipPath></defs><image href={staticFile(avatar)} x={x-size/2} y={top} width={size} height={size} preserveAspectRatio="xMidYMid slice" clipPath={`url(#${id})`}/><text data-account-name="true" x={x} y={nameY} textAnchor="middle" fontFamily="Head" fontSize={32} fill={ink}>{account}</text></g>;
}
