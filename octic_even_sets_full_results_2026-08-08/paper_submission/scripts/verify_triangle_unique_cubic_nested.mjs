function assert(c,m){if(!c)throw new Error(m)}
function mul(a,b){const c=Array(a.length+b.length-1).fill(0);for(let i=0;i<a.length;i++)for(let j=0;j<b.length;j++)c[i+j]+=a[i]*b[j];return c}
function ci(ds){let h=[1];for(const d of ds)h=mul(h,Array(d).fill(1));return h}
function C(n,k){if(k<0||k>n)return 0;k=Math.min(k,n-k);let r=1;for(let i=1;i<=k;i++)r=r*(n-k+i)/i;return Math.round(r)}
function mac(h,d){if(h===0)return 0;let rem=h,prev=1e9,o=0;for(let k=d;k>=1;k--){let a=Math.min(prev-1,rem+k+10);while(a>=k&&C(a,k)>rem)a--;if(a>=k){rem-=C(a,k);o+=C(a+1,k+1);prev=a}else prev=k}return o}
function isO(h){if(h[0]!==1||h[1]>3)return false;for(let d=1;d<h.length-1;d++)if(h[d+1]>mac(h[d],d))return false;let z=false;for(const x of h){if(z&&x!==0)return false;if(x===0)z=true}return true}

const h344=ci([3,4,4]);
const h234=ci([2,3,4]);
const h223=ci([2,2,3]);
const A={
  3:[1,3,6,9,10,2,1,0,0,0],
  4:[1,3,6,9,9,3,1,0,0,0],
  5:[1,3,6,9,8,4,1,0,0,0],
  6:[1,3,6,9,7,5,1,0,0,0]
};
const expectedT={
  3:[1,3,5,7,0,0,0,0,0],
  4:[1,3,5,6,1,0,0,0,0],
  5:[1,3,5,5,2,0,0,0,0],
  6:[1,3,5,4,3,0,0,0,0]
};
const expectedR={
  4:[1,3,4,0,0,0,0],
  5:[1,3,3,1,0,0,0],
  6:[1,3,2,2,0,0,0]
};
for(const d of [3,4,5,6]){
  const s=h344.length-1;
  const T=h344.map((v,i)=>v-A[d][s-i]);
  assert(JSON.stringify(T)===JSON.stringify(expectedT[d]),`bad T for delta ${d}`);
  if(d>=4){
    const s2=h234.length-1;
    const R=h234.map((v,i)=>v-T[s2-i]);
    assert(JSON.stringify(R)===JSON.stringify(expectedR[d]),`bad R for delta ${d}`);
    assert(isO(R),`R should be O-sequence for delta ${d}`);
  }
}
assert(JSON.stringify(expectedR[5].slice(0,4))===JSON.stringify(ci([2,2,2])),'delta=5 residual should be CI(2,2,2)');
const R6=expectedR[6];
const s3=h223.length-1;
const E6=h223.map((v,i)=>v-R6[s3-i]);
assert(JSON.stringify(E6)===JSON.stringify([1,1,2,0,0]),`unexpected delta=6 third residual ${E6}`);
assert(!isO(E6),'(1,1,2) must violate Macaulay growth');
console.log('Unique-cubic nested liaison OK: delta 4/5/6 residual-8 vectors verified; delta=5 gives CI(2,2,2); delta=6 generic CI(2,2,3) residual would be illegal (1,1,2).');
