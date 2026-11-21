import type React from 'react';
import {AbsoluteFill,staticFile} from 'remotion';
import {C,T} from './theme';
import {CoverBrand} from './CoverBrand';
import {cleanCaption} from './captions';
export function WideStage({title,caption,cover,note='',children}:{title:string;caption:string;cover:boolean;note?:string;children:React.ReactNode}){void note;return <AbsoluteFill style={{background:C.bg}}><style>{`@font-face{font-family:Head;src:url('${staticFile('head.woff')}')}`}</style><svg width="1920" height="1080" viewBox="0 0 1920 1080"><rect width="1920" height="12" fill={C.lime}/>{cover?<CoverBrand x={960} top={25} size={85} nameY={148}/>:<><T x={960} y={155} s={45}>{title}</T></>}{children}<path d="M360 934h1200" stroke={C.gold} strokeWidth={2} opacity={.5}/><T x={960} y={999} s={44}>{cleanCaption(caption)}</T></svg></AbsoluteFill>}
