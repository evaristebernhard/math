"""Replot the exploratory data shipped with the paper.

The CSV is numerical continuation data, NOT an interval certificate.
The rigorous proof uses proof/certify_seven.py.
"""
from pathlib import Path
import csv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
datafile = ROOT / "paper" / "figures" / "response_data.csv"
rows = list(csv.DictReader(datafile.open(encoding="utf-8")))
xi = [float(x["xi"]) for x in rows]
lam = [float(x["scaled_lambda"]) for x in rows]
res = [float(x["T_minus_rho"]) for x in rows]
roots = [0.007659607, 0.037207634, 0.065677290]
turns = [0.00427530, 0.02615002, 0.04964750]
outdir = ROOT / "paper" / "figures"
outdir.mkdir(parents=True, exist_ok=True)
fig, ax = plt.subplots(figsize=(9,4.2))
ax.plot(xi, lam, lw=1.7, label="numerical response")
ax.axhline(0,ls="--",lw=.85)
for q in turns: ax.axvline(q,ls=":",lw=.8,alpha=.6)
ax.scatter(roots,[0]*3,marker="x",s=62,zorder=3)
ax.grid(alpha=.25)
ax.set(xlabel="Mean xi",ylabel="1e5 Lambda(xi)",title="Seven-cycle witness: three positive response zeros")
fig.tight_layout()
fig.savefig(outdir/"response.png",dpi=180)
plt.close(fig)
fig, ax = plt.subplots(figsize=(9,4.2))
ax.plot(xi,res,lw=1.7)
ax.axhline(0,ls="--",lw=.85)
for q in turns: ax.axvline(q,ls=":",lw=.8,alpha=.6)
ax.grid(alpha=.25)
ax.set(xlabel="Mean xi",ylabel="T(xi) - rho",title="Residence-time mechanism")
fig.tight_layout()
fig.savefig(outdir/"residence.png",dpi=180)
plt.close(fig)
print("Saved exploratory plots to",outdir)
