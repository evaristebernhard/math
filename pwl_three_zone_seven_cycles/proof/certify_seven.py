"""Independent decimal-directed + rational Taylor interval audit.
No SciPy, mpmath or floating point needed to decide six Poincare signs.

Assumptions: Python Decimal obeys specified directed rounding (ROUND_FLOOR /
ROUND_CEILING). All trig and exponential evaluations use explicitly bounded
Taylor polynomials; pi is bounded using exact rational Machin arctangent sums.
This certificate is independent of seven_cycle_interval_witness.py.
"""
from decimal import Decimal as D, localcontext, getcontext, ROUND_FLOOR, ROUND_CEILING
from dataclasses import dataclass
from fractions import Fraction
from math import factorial

getcontext().prec=95

def calc(f,mode):
    with localcontext() as ctx:
        ctx.prec=95;ctx.rounding=mode
        return f()

def below(f):return calc(f,ROUND_FLOOR)
def above(f):return calc(f,ROUND_CEILING)

def dec(v):
    if isinstance(v,D):return v
    return D(str(v))

@dataclass
class I:
    l:D
    r:D
    def __post_init__(self):
        assert self.l<=self.r,(self.l,self.r)
    @classmethod
    def v(cls,v):
        if isinstance(v,cls):return v
        x=dec(v);return cls(x,x)
    @classmethod
    def fract(cls,f):
        if not isinstance(f,Fraction):f=Fraction(f)
        return cls(below(lambda:D(f.numerator)/D(f.denominator)),above(lambda:D(f.numerator)/D(f.denominator)))
    def __add__(self,b):
        b=I.v(b)
        return I(below(lambda:self.l+b.l),above(lambda:self.r+b.r))
    __radd__=__add__
    def __neg__(self):return I(-self.r,-self.l)
    def __sub__(self,b):return self+-I.v(b)
    def __rsub__(self,b):return I.v(b)+-self
    def __mul__(self,b):
        b=I.v(b)
        vals=[(u,v) for u in (self.l,self.r) for v in (b.l,b.r)]
        return I(min(below(lambda:u*v) for u,v in vals),max(above(lambda:u*v) for u,v in vals))
    __rmul__=__mul__
    def inv(self):
        assert not (self.l<=0<=self.r),self
        return I(below(lambda:D(1)/self.r),above(lambda:D(1)/self.l))
    def __truediv__(self,b):return self*I.v(b).inv()
    def __rtruediv__(self,b):return I.v(b)*self.inv()
    def pad(self,eps):return I(below(lambda:self.l-eps),above(lambda:self.r+eps))
    def sign(self):return '+' if self.l>0 else '-' if self.r<0 else '?'
    def contains(self,x):return self.l<=dec(x)<=self.r
    def __str__(self):return f'[{self.l},{self.r}]'

# Exact Machin formula pi=16 arctan(1/5)-4 arctan(1/239)
def atan_bounds(k,n=65):
    low=sum(((-1)**j)*Fraction(1,(2*j+1)*k**(2*j+1)) for j in range(n))
    next_term=Fraction(1,(2*n+1)*k**(2*n+1))
    if n%2==0:return low,low+next_term
    return low-next_term,low
l5,h5=atan_bounds(5);l239,h239=atan_bounds(239)
PI=I(I.fract(16*l5-4*h239).l,I.fract(16*h5-4*l239).r)
PI2=2*PI

# For all function arguments |x|<=10.
# sin and cos: Taylor remainder magnitude <= 10^161/161! by
# Taylor's theorem, since all derivatives are <=1 on the real line.
# exp: <= e^10*10^161/161! < 3^10*10^161/161!.
# Both are < 1e-95 for 161 terms.
assert 3**10 * 10**161 * 10**95 < factorial(161)
REM=D('1e-95')

def taylor_exp(x):
    x=I.v(x)
    assert -10<x.l and x.r<10,(x,'exp argument')
    term=I.v(1);p=I.v(1)
    for k in range(1,161):
        term=(term*x)/k
        p=p+term
    return p.pad(REM)

def taylor_sin(x):
    x=I.v(x)
    assert -10<x.l and x.r<10
    term=x;p=term
    xx=-(x*x)
    for k in range(1,81):
        term=term*xx/((2*k)*(2*k+1))
        p=p+term
    return p.pad(REM)

def taylor_cos(x):
    x=I.v(x)
    assert -10<x.l and x.r<10
    term=I.v(1);p=term
    xx=-(x*x)
    for k in range(1,81):
        term=term*xx/((2*k-1)*(2*k))
        p=p+term
    return p.pad(REM)

A=D('9');B=D('1.5');MU=D('1.81363')
regions={'middle':(D('-1.5'),D('0')),'lower':(D('9'),D('10.5')),'upper':(D('9'),D('-10.5'))}

def flow(t0,y0,t,c,d):
    t0,y0,t=I.v(t0),I.v(y0),I.v(t)
    h=t-t0; e=taylor_exp(-c*h)
    a=I.v(MU)/(1+c*c)
    # same exact physical solution, independently evaluated transcendental terms
    return (e*y0) - (I.v(d)/c)*(1-e) + a*((c*taylor_sin(t)-taylor_cos(t)) - e*(c*taylor_sin(t0)-taylor_cos(t0)))

# Rational decimal centers of candidate events, generated separately with
# high precision, not accepted as evidence until exact sign enclosures pass.
EV={
'-0.571':['0.690900167350795596241598610060','1.078135763256395127520565407613','3.717538493711361911132150876164','4.228305204642255023584881326373'],
'-0.567':['0.727167718353076856080532101227','1.073698524509500870150051069731','3.677514848910453028389655375076','4.230022149628273629974937792239'],
'-0.55677':['0.943026106870525525503040801495','1.000234039978349548083465355225','3.432412794615143204771577791489','4.234378779776890243529064894432'],
'-0.55675':['0.945709233396853423992784093457','0.998251562666127082230286839438','3.430444659672579159693512100466','4.234391508369720611532563245294'],
'-0.5552':['3.236980253181229129925056035276','4.235050045133705101139984519530'],
'-0.5545':['3.174998296322684715262752036462','4.235124128244673521022306819212'],
'-0.55517':['3.234089094501122628580828533598','4.235054342221641269610541466055'],
'-0.55514':['3.231221607277306682192172796767','4.235058511047931109063368566348'],
}
MIN={
'-0.5552':'0.964791284430258571470380435247',
'-0.5545':'0.960497483306786195849686316059',
'-0.55517':'0.964606148956481813734238900023',
'-0.55514':'0.964421114280833615237799576884'
}

def span(center,r):return I(dec(center)-dec(r),dec(center)+dec(r))

def check(ytext):
    ys=I.v(ytext)
    four=len(EV[ytext])==4
    zones=['middle','lower','middle','upper','middle'] if four else ['middle','upper','middle']
    levels=[D(-1),D(-1),D(1),D(1)] if four else [D(1),D(1)]
    widths=['1e-27','1e-22','1e-19','1e-12'] if four else ['1e-27','1e-19']
    prev_t=I.v(0);prev_y=ys
    vels=[];events=[]
    for j,(cs,level,width) in enumerate(zip(EV[ytext],levels,widths)):
        c,d=regions[zones[j]]
        te=span(cs,width)
        vl=flow(prev_t,prev_y,I.v(te.l),c,d)-level
        vr=flow(prev_t,prev_y,I.v(te.r),c,d)-level
        assert vl.sign()!='?' and vr.sign()!='?' and vl.sign()!=vr.sign(),(ytext,j,vl,vr)
        speed=I.v(MU)*taylor_sin(te)+I.v(B)*level
        expected=['-','+','+','-'][j] if four else ['+','-'][j]
        assert speed.sign()==expected,(ytext,j,speed)
        vels.append(speed.sign());events.append(te)
        prev_t=te;prev_y=I.v(level)
    # Check interval positions used in the first-hit shape argument.
    if four:
        assert events[1].r<(PI/2).l and events[2].l>PI.r and events[3].r<(3*PI/2).l
    else:
        assert events[0].l>PI.r and events[1].r<(3*PI/2).l
    c,d=regions[zones[-1]]
    disp=flow(prev_t,prev_y,PI2,c,d)-ys
    assert disp.sign()!='?',(ytext,disp)
    # The last middle-zone flight stays above -1 since its velocity is
    # negative throughout, and final state >-1; follows from q monotonicity.
    final_x=disp+ys
    assert final_x.l>-1,(ytext,final_x)
    if not four:
        tm=span(MIN[ytext],'1e-22')
        c,d=regions['middle']
        va=I.v(MU)*taylor_sin(I.v(tm.l))-c*flow(I.v(0),ys,I.v(tm.l),c,d)-d
        vb=I.v(MU)*taylor_sin(I.v(tm.r))-c*flow(I.v(0),ys,I.v(tm.r),c,d)-d
        assert va.sign()=='-' and vb.sign()=='+',(ytext,va,vb)
        lo_x=flow(I.v(0),ys,tm,c,d)
        assert lo_x.l>-1,(ytext,lo_x)
    # A terminal middle flight cannot make an extra downward crossing: \n    # q=e^{c(t-t0)}u' decreases until 3pi/2 and then increases; \n    # its values at t_last and 2pi are both negative.
    terminal_v=I.v(MU)*taylor_sin(PI2)+I.v(B)*final_x
    assert terminal_v.sign()=='-',(ytext,terminal_v)
    return disp,events,vels


# Independent half-period brackets for the antisymmetric center. The short
# rational initial-value interval is chosen for a nonunit multiplier certificate.
CENTER_EV={
'-0.579022471':[
 '0.634581372314921880292542675282205728',
 '1.083171326123873562346343278450922288'],
'-0.579022470':[
 '0.634581378413117209211221821647541674',
 '1.083171325676822885739904090457136619'],
}
def center_half(ytext):
    y=I.v(ytext)
    t0=I.v(0);x0=y
    events=[]
    for (cent,wid,zone,direction) in zip(CENTER_EV[ytext],
            ['1e-27','1e-22'],['middle','lower'],['-','+']):
        c,d=regions[zone]
        hit=span(cent,wid)
        va=flow(t0,x0,I.v(hit.l),c,d)+1
        vb=flow(t0,x0,I.v(hit.r),c,d)+1
        assert va.sign()!='?' and vb.sign()!='?' and va.sign()!=vb.sign(),(ytext,zone,va,vb)
        speed=I.v(MU)*taylor_sin(hit)-I.v(B)
        assert speed.sign()==direction,(ytext,zone,speed)
        events.append(hit); t0=hit;x0=I.v(-1)
    upi=flow(t0,x0,PI,*regions['middle'])
    assert upi.l>-1 and upi.r<1
    q=upi+y
    assert q.sign()!='?'
    s=events[1]-events[0]
    return q,s


# The only possible grazing phases at the levels +-1 are independent of y.
# These rational centers were generated by an external high-precision solver;
# they are accepted only after strict opposite signs of the LEVEL VELOCITY.
GRAZE_PHASES = [
    ('0.973875926376460045824009680088', '-1', '-'),
    ('2.167716727213333192638633703191', '-1', '+'),
    ('4.115468579966253284286653063368', '1', '+'),
    ('5.309309380803126431101277086471', '1', '-'),
]

def check_grazing_barrier(ytext):
    """Sign of x(t_*,y)-level at each tangency-eligible forcing phase.

    Combined with scalar order between adjacent rational shooting endpoints,
    a strict sign for both endpoints rules out a grazing parameter anywhere
    in their closed shooting interval.
    """
    initial=I.v(ytext)
    _,events,_=check(ytext)
    four=len(events)==4
    zones=['middle','lower','middle','upper','middle'] if four else ['middle','upper','middle']
    levels=[I.v(-1),I.v(-1),I.v(1),I.v(1)] if four else [I.v(1),I.v(1)]
    results=[]
    for center,level,direction in GRAZE_PHASES:
        tg=span(center,'1e-25')
        # Exact tangency time is inside tg by a sign change of level velocity.
        v_left=I.v(MU)*taylor_sin(I.v(tg.l))+I.v(B)*I.v(level)
        v_right=I.v(MU)*taylor_sin(I.v(tg.r))+I.v(B)*I.v(level)
        assert v_left.sign()!='?' and v_right.sign()!='?' and v_left.sign()!=v_right.sign(),(center,v_left,v_right)
        j=sum(e.r < tg.l for e in events)
        assert 0<=j<len(zones) and (j==len(events) or tg.r<events[j].l),(ytext,center,j)
        t0=I.v(0) if j==0 else events[j-1]
        y0=initial if j==0 else levels[j-1]
        c,d=regions[zones[j]]
        gap=flow(t0,y0,tg,c,d)-I.v(level)
        assert gap.sign()!='?',(ytext,center,gap)
        expected=('-' if four else '+') if level=='-1' and direction=='-' else ('+' if level=='-1' else ('+' if direction=='+' else '-'))
        # For four-crossing lower case, later lower phase is above -1.
        assert gap.sign()==expected,(ytext,center,level,gap.sign(),expected)
        results.append(gap)
    return results


if __name__=='__main__':
    print('Pi enclosure',str(PI)[:100])
    for pair in [('-0.571','-0.567'),('-0.55677','-0.55675'),('-0.55517','-0.55514')]:
        result=[]
        for y in pair:
            di,_,_=check(y)
            print('D(',y,')=',di,'width',di.r-di.l)
            result.append(di.sign())
        assert result in (['+','-'],['-','+'])
    # Half-period antisymmetric center y_c is below first bracket:
    # Q(y)=u(pi;y)+y is strictly increasing. For y=-0.571, the
    # trajectory has exactly two lower-level hits prior to pi.
    _,ev,_=check('-0.571')
    upi=flow(ev[1],I.v(-1),PI,*regions['middle'])
    qcenter=upi+I.v('-0.571')
    assert -1<upi.l and upi.r<1
    assert qcenter.sign()=='+'
    print('Q(-0.571) = u(pi; -0.571) -0.571',qcenter)
    for left,right in [('-0.571','-0.567'),('-0.55677','-0.55675'),('-0.55517','-0.55514')]:
        gaps_left=check_grazing_barrier(left)
        gaps_right=check_grazing_barrier(right)
        assert [g.sign() for g in gaps_left]==[g.sign() for g in gaps_right]
        print('Grazing barriers',left,right,[g.sign() for g in gaps_left])
    qlo,slo=center_half('-0.579022471')
    qhi,shi=center_half('-0.579022470')
    assert qlo.sign()=='-' and qhi.sign()=='+'
    # The first descending -1 crossing moves right as the initial value
    # increases, and the second ascending crossing moves left. Consequently
    # the lower-zone residence length decreases with shooting initial value.
    # On the antisymmetric orbit, each outer zone is visited for length s,
    # hence log(P') = 3*pi - 21*s. The lower bracket gives the largest s.
    assert slo.r < (PI/I.v(7)).l,(slo,PI/I.v(7))
    print('center Q bracket',qlo,qhi)
    print('center s upper',slo.r,'pi/7 lower',(PI/I.v(7)).l)
    print('CERTIFIED SIGNS, center ordering, and nonunit center multiplier: >= 7 isolated cycles')