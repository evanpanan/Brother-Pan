import {C,T,R,V,L} from '../theme';
/** Hypothetical balance sheet, not a margin-call model. Interest/taxes/early liquidation excluded. */
export function DebtEquity({t,own=5,debt=5,drop=.4,start=3,end=9}:{t:number;own?:number;debt?:number;drop?:number;start?:number;end?:number}){
 if(own<=0||debt<0||drop<0||drop>1||![own,debt,drop].every(Number.isFinite)||end<=start)throw new Error('Invalid illustrative balance sheet');
 const initial=own+debt,q=V(t,start,end),assets=L(initial,initial*(1-drop),q),equity=assets-debt,base=1080,unit=500/initial,debtH=Math.min(assets,debt)*unit,eqH=Math.max(0,equity)*unit,loss=(equity/own-1)*100;
 return <g><T y={480} s={35}>自有 {own}万 ＋ 借款 {debt}万</T><R x={225} y={base-debtH} w={245} h={debtH} c={C.gold} r={0}/><R x={225} y={base-debtH-eqH} w={245} h={eqH} c={C.lime} r={0}/><T x={347} y={base-debtH-eqH-30} s={44}>资产 {assets.toFixed(1)}万</T><T x={347} y={base-debtH/2+12} s={33}>债务 {debt}万</T><R x={585} y={620} w={320} h={400} c={C.ink}/><T x={745} y={700} s={31} c={C.white}>你的净值</T><T x={745} y={790} s={58} c={C.lime}>{equity.toFixed(1)}万</T><T x={745} y={900} s={35} c={C.white}>本金 {loss.toFixed(0)}%</T><T y={1170} s={31}>资产跌 {(drop*100).toFixed(0)}% 不等于本金只跌 {(drop*100).toFixed(0)}%</T><T y={1240} s={24}>假设示例 忽略利息 税费与提前强平</T></g>;
}
