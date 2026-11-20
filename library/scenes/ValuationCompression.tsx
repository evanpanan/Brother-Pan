import {C,T,R,V} from '../theme';
/** Scenario only: revenue × price-to-sales multiple. Never infers a target price. */
export function ValuationCompression({t,revenueBefore=100,revenueAfter=150,multipleBefore=20,multipleAfter=10}:{t:number;revenueBefore?:number;revenueAfter?:number;multipleBefore?:number;multipleAfter?:number}){
 const before=revenueBefore*multipleBefore,after=revenueAfter*multipleAfter;
 if(![revenueBefore,revenueAfter,multipleBefore,multipleAfter].every(Number.isFinite)||revenueBefore<=0||multipleBefore<=0||revenueAfter<0||multipleAfter<0)throw new Error('Invalid scenario inputs');
 const pct=(x:number)=>`${x>=0?'+':''}${Math.round(x*100)}%`;
 return <g><R x={170} y={470} w={340} h={170} c={C.lime}/><T x={340} y={540} s={32}>收入</T><T x={340} y={605} s={48}>{revenueBefore} → {revenueAfter}</T><R x={570} y={470} w={340} h={170} c={C.pale}/><T x={740} y={540} s={32}>市销率</T><T x={740} y={605} s={48}>{multipleBefore} → {multipleAfter}</T><g opacity={V(t,.1,.7)}><path d="M540 715v80m-22-22 22 22 22-22" stroke={C.gold} strokeWidth={8} fill="none"/></g><g opacity={V(t,1.5,2.4)}><R x={180} y={870} w={720} h={240} c={C.ink}/><T y={965} s={48} c={C.white}>估值 {before} → {after}</T><T y={1045} s={39} c={C.lime}>收入 {pct(revenueAfter/revenueBefore-1)}  估值 {pct(after/before-1)}</T></g><T y={1210} s={25}>假设情景 非具体公司实际估值或目标价</T></g>;
}
