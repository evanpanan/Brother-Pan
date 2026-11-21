import type React from 'react';
import {AbsoluteFill,staticFile} from 'remotion';
import {C,T} from './theme';
import {cleanCaption} from './captions';
import {CoverBrand} from './CoverBrand';
export function Stage({title,caption='',brand='',cover=false,account='华尔街潘哥',children}:{title:string;caption?:string;brand?:string;cover?:boolean;account?:string;children:React.ReactNode}){
 void brand;
 const text=cleanCaption(caption),letters=Array.from(text),half=Math.ceil(letters.length/2),lines=letters.length>15?[letters.slice(0,half).join(''),letters.slice(half).join('')]:[text];
 return <AbsoluteFill style={{background:C.bg}}><style>{`@font-face{font-family:Head;src:url('${staticFile('head.woff')}')}`}</style><svg viewBox="0 0 1080 1920"><rect width="1080" height="20" fill={C.lime}/>{cover?<CoverBrand account={account}/>:<><T y={330} s={42}>{title}</T></>}{children}<path d="M240 1300H840" stroke={C.gold} strokeWidth="3" opacity=".4"/><g data-caption-region="true">{lines.map((line,i)=><T key={i} y={lines.length>1?1365+i*65:1400} s={44}>{line}</T>)}</g></svg></AbsoluteFill>;
}
