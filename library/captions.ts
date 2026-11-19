const punct=/\p{P}/u;
const digit=(s:string)=>/[0-9０-９]/u.test(s);
const letter=(s:string)=>/[A-Za-z]/.test(s);
/** Display only: never pass this cleaned string to speech synthesis. */
export function cleanCaption(text:string):string {
 const chars=Array.from(text),out:string[]=[];
 chars.forEach((ch,i)=>{const a=chars[i-1]||'',b=chars[i+1]||'';
  if(ch==='?'||ch==='？'){out.push('？');return;}
  if(ch==='%'||ch==='％'||ch==='/'){out.push(ch);return;}
  if(((ch==='.'||ch==='．'||ch===':'||ch==='：')&&digit(a)&&digit(b))||(ch==='.'&&letter(a)&&letter(b))){out.push(ch==='．'?'.':ch==='：'?':':ch);return;}
  if((ch==='-'||ch==='−')&&digit(b)){out.push(ch);return;}
  if(/[–—~～]/u.test(ch)&&(/[0-9０-９%％]/u.test(a))&&digit(b)){out.push('至');return;}
  if((ch==='-'||ch==="'"||ch==='’')&&letter(a)&&letter(b)){out.push(ch);return;}
  if(!punct.test(ch)){out.push(ch);}
 });
 return out.join('').replace(/\s+/g,' ').trim();
}
export type Caption={text:string;startMs:number;endMs:number};
export const currentCaption=(caps:Caption[],ms:number)=>caps.find(c=>ms>=c.startMs&&ms<c.endMs);
