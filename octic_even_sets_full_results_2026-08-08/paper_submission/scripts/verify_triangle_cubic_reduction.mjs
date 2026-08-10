function assert(cond, msg) { if (!cond) throw new Error(msg); }
function comb(n,k){ if(k<0||k>n)return 0; k=Math.min(k,n-k); let r=1; for(let i=1;i<=k;i++)r=r*(n-k+i)/i; return Math.round(r); }
function mul(a,b){ const c=Array(a.length+b.length-1).fill(0); for(let i=0;i<a.length;i++)for(let j=0;j<b.length;j++)c[i+j]+=a[i]*b[j]; return c; }
function macNext(h,d){ if(h===0)return 0; let rem=h,prev=1e9,out=0; for(let k=d;k>=1;k--){ let a=Math.min(prev-1,rem+k+10); while(a>=k&&comb(a,k)>rem)a--; if(a>=k){rem-=comb(a,k);out+=comb(a+1,k+1);prev=a;}else prev=k;} return out; }
function isO(h){ if(h[0]!==1||h[1]>3)return false; for(let d=1;d<h.length-1;d++)if(h[d+1]>macNext(h[d],d))return false; let z=false; for(const x of h){if(z&&x!==0)return false;if(x===0)z=true;} return true; }
function ciH(ds){let h=[1];for(const d of ds)h=mul(h,Array(d).fill(1));return h;}

const h444=ciH([4,4,4]);
const candidates=[];
for(let h1=0;h1<=3;h1++)for(let h2=0;h2<=6;h2++)for(let h3=0;h3<=10;h3++)for(let h4=0;h4<=12;h4++){
  const h=[1,h1,h2,h3,h4,12-h4,10-h3,6-h2,3-h1,0];
  if(Math.min(...h)<0||!isO(h))continue;
  const d=32-h.slice(0,5).reduce((a,b)=>a+b,0);
  if(d<2)continue;
  let e=null;for(let t=0;t<=4;t++){const H=h.slice(0,t+1).reduce((a,b)=>a+b,0);if(comb(t+3,3)-H>0){e=t;break;}}
  candidates.push({h,d,e});
}
const cubic=candidates.filter(x=>x.e===3);
assert(cubic.length===18,`expected 18 cubic candidates, got ${cubic.length}`);

const table=cubic.map(({h,d})=>({d,m3:10-h[3],I4:3+d,h})).sort((a,b)=>a.d-b.d||a.m3-b.m3);
const expectedPairs=['2:1','3:1','4:1','4:2','5:1','5:2','6:1','6:2','6:3','7:1','7:2','7:3','8:2','8:3','9:3','9:4','10:4','11:5'];
assert(JSON.stringify(table.map(x=>`${x.d}:${x.m3}`))===JSON.stringify(expectedPairs),'unexpected (delta,m3) list');

// If m3>=2 and the cubic system has no fixed divisor, choose two coprime cubics
// and a quartic to obtain a CI(3,3,4).  The residual length is 4.
const h334=ciH([3,3,4]);
const coprimeResults=[];
for(const x of table.filter(x=>x.m3>=2)){
  const s=h334.length-1;
  const hE=h334.map((v,i)=>v-(x.h[s-i]??0));
  const ok=Math.min(...hE)>=0&&isO(hE);
  coprimeResults.push({...x,hE,ok});
}
const survivors=coprimeResults.filter(x=>x.ok);
assert(survivors.length===1,'expected one coprime-pencil survivor');
assert(survivors[0].d===7&&survivors[0].m3===2,'survivor should be delta=7,m3=2');
assert(JSON.stringify(survivors[0].hE)===JSON.stringify([1,1,1,1,0,0,0,0]),'residual should be four collinear points');

// Unique-cubic candidates: for delta>=3 the quotient I_A(4)/(p*S1) has dimension delta-1,
// so for delta>=3 we can choose two quartics modulo p and form a CI(3,4,4).
const h344=ciH([3,4,4]);
const unique=[];
for(const x of table.filter(x=>x.m3===1&&x.d>=3)){
  const s=h344.length-1;
  const hT=h344.map((v,i)=>v-(x.h[s-i]??0));
  unique.push({...x,hT,ok:Math.min(...hT)>=0&&isO(hT)});
}
const uniqueOK=unique.filter(x=>x.ok).map(x=>x.d);
assert(JSON.stringify(uniqueOK)===JSON.stringify([3,4,5,6]),`unexpected unique-cubic CI344 survivors ${uniqueOK}`);
const d7=unique.find(x=>x.d===7);
assert(d7&&!d7.ok,'delta=7 unique cubic should fail CI344 liaison');

console.log('Higher cubic audit OK: 18 candidates; coprime m3>=2 leaves only (delta,m3)=(7,2) with residual h=(1,1,1,1); unique-cubic CI(3,4,4) leaves delta=3,4,5,6 and kills delta=7.');
