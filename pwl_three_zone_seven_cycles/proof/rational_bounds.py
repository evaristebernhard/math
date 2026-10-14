"""Optional exact-rational audit of the inequalities printed in the manuscript.

Uses Fraction endpoints on the rational lattice 10**(-80). It shares the
flight structure and rational event inputs with certify_seven.py; the
arithmetic backend has no Decimal or floating-point rounding premise.
Floating-point conversions below are for display only. The manuscript
states its inequalities and all mathematical deductions independently.
"""
from fractions import Fraction as F
import importlib.util,json
from pathlib import Path
spec=importlib.util.spec_from_file_location('old',Path(__file__).with_name('certify_seven.py'))
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
S=10**80
def frac(v):return v if isinstance(v,F) else F(str(v))
def lo(v):return F((v*S).__floor__(),S)
def hi(v):return F((v*S).__ceil__(),S)
class I:
 def __init__(self,l,r):
  self.l,self.r=frac(l),frac(r);assert self.l<=self.r
 @classmethod
 def v(cls,v):return v if isinstance(v,cls) else cls(v,v)
 @classmethod
 def fract(cls,v):return cls(lo(frac(v)),hi(frac(v)))
 def __add__(self,b):
  b=I.v(b);return I(lo(self.l+b.l),hi(self.r+b.r))
 __radd__=__add__
 def __neg__(self):return I(-self.r,-self.l)
 def __sub__(self,b):return self+-I.v(b)
 def __rsub__(self,b):return I.v(b)+-self
 def __mul__(self,b):
  b=I.v(b);vs=[u*v for u in (self.l,self.r) for v in (b.l,b.r)]
  return I(lo(min(vs)),hi(max(vs)))
 __rmul__=__mul__
 def inv(self):
  assert not self.l<=0<=self.r
  return I(lo(1/self.r),hi(1/self.l))
 def __truediv__(self,b):return self*I.v(b).inv()
 def __rtruediv__(self,b):return I.v(b)*self.inv()
 def pad(self,eps):return I(lo(self.l-frac(eps)),hi(self.r+frac(eps)))
 def sign(self):return '+' if self.l>0 else '-' if self.r<0 else '?'
 def contains(self,v):return self.l<=frac(v)<=self.r
 def __str__(self):return str([float(self.l),float(self.r)])
m.I=I
a,b=m.atan_bounds(5);c,d=m.atan_bounds(239)
m.PI=I(lo(16*a-4*d),hi(16*b-4*c))
m.PI2=2*m.PI
def bounds(q):return [float(q.l),float(q.r)]
def main():
 ys=['-0.571','-0.567','-0.55677','-0.55675','-0.55517','-0.55514']
 out={}
 for y in ys:
  disp,events,vels=m.check(y)
  gaps=m.check_grazing_barrier(y)
  out[y]={'D':bounds(disp),'events':[bounds(e) for e in events],'gaps':[bounds(g) for g in gaps]}
  assert disp.sign()==dict(zip(ys,['+','-','-','+','+','-']))[y]
  enclosing=[('1.13334e-5','1.13357e-5'),('-2.57304e-5','-2.57281e-5'),('-4.97010e-6','-4.96788e-6'),('5.38442e-6','5.38665e-6'),('9.31073e-6','9.31075e-6'),('-1.07074e-5','-1.07072e-5')][ys.index(y)]
  assert F(enclosing[0])<disp.l<=disp.r<F(enclosing[1])
  assert all(min(abs(g.l),abs(g.r))>F(3,10000) for g in gaps)
  print(y,out[y],flush=True)
 out['center']={}
 for y in m.CENTER_EV:
  q,s=m.center_half(y);out['center'][y]={'Q':bounds(q),'s':bounds(s)}
  assert q.sign()==('-' if y.endswith('471') else '+')
  assert s.r<F('0.448589954')<m.PI.l/7
  print('center',y,out['center'][y],flush=True)
 
 example={}
 y='-0.571';prev_t=I.v(0);prev_y=I.v(y)
 for j,(center,width,zone,level) in enumerate(zip(m.EV[y],['1e-27','1e-22','1e-19','1e-12'],['middle','lower','middle','upper'],[-1,-1,1,1]),1):
  hit=m.span(center,width);c,d=m.regions[zone]
  left=m.flow(prev_t,prev_y,I.v(hit.l),c,d)-level
  right=m.flow(prev_t,prev_y,I.v(hit.r),c,d)-level
  example[j]={'left':bounds(left),'right':bounds(right),'speed':bounds(I.v(m.MU)*m.taylor_sin(hit)+F(3,2)*level)}
  prev_t=hit;prev_y=I.v(level)
 print('WORKED EXAMPLE',json.dumps(example),flush=True)
 for y in m.CENTER_EV:
  ev=[m.span(c,w) for c,w in zip(m.CENTER_EV[y],['1e-27','1e-22'])]
  for center,level,direction in m.GRAZE_PHASES[:2]:
   phase=m.span(center,'1e-25');j=sum(e.r<phase.l for e in ev)
   t0=I.v(0) if j==0 else ev[j-1];x0=I.v(y) if j==0 else I.v(-1)
   gap=m.flow(t0,x0,phase,*m.regions[['middle','lower','middle'][j]])+1
   assert gap.sign()==('-' if j==1 else '+')
   print('CENTER GAP',y,center,bounds(gap),flush=True)
 

if __name__=='__main__':
 main()

