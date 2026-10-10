"""Estimate orthogonal ANOVA Fourier projection of bounded quartic p_d.
SINGLETON basis sqrt(2)*cos(theta_j); pair basis 2*cos(theta_i)*cos(theta_j).
These form orthonormal functions of independent uniform theta coordinates.
Estimates are diagnostics ONLY; exact identities rely on martingale property.
"""
import numpy as np
import argparse,json

def estimate(n=65536,d=49,seed=123):
 rng=np.random.default_rng(seed)
 theta=rng.uniform(-np.pi,np.pi,(n,d)); C=np.cos(theta)
 p=C[:,0].copy(); singles=np.zeros(d);pairs=np.zeros((d,d));odd_two_one=np.zeros((d,d));singles[0]=1/np.sqrt(2)
 for j in range(1,d):
  z=1-p*p
  inc=.5*z+.125*z*z
  singles[j]=np.mean(inc)/np.sqrt(2)
  pairs[:j,j]=C[:,:j].T @inc / n
  odd_two_one[:j,j]=(2*C[:,:j]**2-1).T @ inc / n
  p+=inc*C[:,j]
 return singles,pairs,odd_two_one,np.mean(p*p)

if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--samples',type=int,default=65536);a.add_argument('--out',default='teacher_projection.json');args=a.parse_args()
 e1,p1,o1,m1=estimate(args.samples,seed=149);e2,p2,o2,m2=estimate(args.samples,seed=280)
 cross=float(e1@e2+np.sum(p1*p2));sing=float(e1@e2)
 diag={'samples_per_replica':args.samples,'M49_replica':[float(m1),float(m2)], 'singleton_energy_cross':sing,
       'singleton_plus_pairs_energy_cross':cross,'top_pair_modes':[],
       'warning':'Monte Carlo; cross-replica dot products reduce coefficient squared-noise bias; not certified.'}
 idx=np.dstack(np.unravel_index(np.argsort(np.abs(p1*p2).ravel())[::-1],p1.shape))[0]
 for i,j in idx:
  if i>=j: continue
  diag['top_pair_modes'].append({'i':int(i+1),'j':int(j+1),'a':float(p1[i,j]),'replica_b':float(p2[i,j]),'energy':float(p1[i,j]*p2[i,j])})
  if len(diag['top_pair_modes'])>=12: break
 # Estimated importance ordering of orthogonal teacher modes, with Fourier pair cost.
 groups=[(float(e1[i]*e2[i]),1,'singleton',int(i+1),0) for i in range(len(e1))]
 groups += [(float(o1[i,j]*o2[i,j]),2,'2e_i+e_j',int(i+1),int(j+1)) for i in range(len(e1)) for j in range(i+1,len(e1))]
 groups.sort(reverse=True)
 for budget in [4,8,16,24,40,64,100,200,400,1000,2401]:
  take=[];spent=0;energy=0
  for val,cost,kind,i,j in groups:
   if spent+cost>budget: continue
   spent+=cost;energy+=val
   if spent>=budget:break
  diag.setdefault('cumulative_energy_by_sign_pair_budget',{})[str(budget)]=float(energy)
 diag['top_teacher_groups']=[{'gain':v,'frequency_pairs':cost,'kind':kind,'i':i,'j':j} for v,cost,kind,i,j in groups[:25]]
 diag["two_one_energy_cross"]=float(np.sum(o1*o2))
 diag["single_plus_two_one_energy_cross"]=sing+diag["two_one_energy_cross"]
 print('M49',m1,m2,'single',sing,'single+pair',cross,'two+one',diag["two_one_energy_cross"],'combined',diag["single_plus_two_one_energy_cross"])
 print('top pairs',diag['top_pair_modes'][:6]);open(args.out,'w').write(json.dumps(diag,indent=2))
