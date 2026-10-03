#!/usr/bin/env python3
"""SortLLM v0.8 deterministic scorer. Usage: python3 score_v08.py input.json"""
import json, re, sys, os
HOUSES=["Gryffindor","Ravenclaw","Hufflepuff","Slytherin"]
SPEC=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"sortllm_pairing_ritual_v08.json"),encoding="utf-8"))
ITEMS={it["id"]:it["options"] for it in SPEC["questionnaire"]["items"]}; POINTS=SPEC["questionnaire"]["rank_points"]
DIMS=sorted({d for opts in ITEMS.values() for o in opts.values() for d in o["dims"]})
def parse_rank(s):
    letters=re.findall(r"[ABCD]",s.upper())
    if sorted(letters)!=["A","B","C","D"]: raise ValueError(f"bad ranking: {s!r}")
    return letters
def questionnaire(runs):
    house={h:0.0 for h in HOUSES}; dim={d:0.0 for d in DIMS}; dim_max={d:0.0 for d in DIMS}
    for run in runs:
        if set(run)!=set(ITEMS): raise ValueError("run must answer all items")
        for qid,ranking in run.items():
            for pos,letter in enumerate(parse_rank(ranking)):
                opt=ITEMS[qid][letter]; house[opt["house"]]+=POINTS[pos]
                for d in opt["dims"]: dim[d]+=POINTS[pos]; dim_max[d]+=POINTS[0]
    total=sum(house.values())
    return ({h:100*v/total for h,v in house.items()},{d:round(100*dim[d]/dim_max[d],1) for d in DIMS})
def behavior(items):
    n=len(items); counts={h:sum(1 for b in items if b["house"]==h) for h in HOUSES}
    return {h:(counts[h]+0.5)/(n+2)*100 for h in HOUSES},n
def side(data):
    q,dims=questionnaire(data["runs"]); b,n=behavior(data.get("behaviors",[])); wq,wb=((0.6,0.4) if n>=5 else (0.8,0.2))
    final={h:wq*q[h]+wb*b[h] for h in HOUSES}; ranked=sorted(HOUSES,key=lambda h:-final[h])
    return {"final":{h:round(final[h],1) for h in HOUSES},"questionnaire":{h:round(q[h],1) for h in HOUSES},"dims":dims,"primary":ranked[0],"second":ranked[1],"n_behaviors":n,"runs":len(data["runs"]),"contaminated":data.get("contaminated",False),"blind":data.get("blind",True)}
def pair(ai,hu,bonding,months):
    p,q=ai["final"],hu["final"]; S=100-0.5*sum(abs(p[h]-q[h]) for h in HOUSES); C=25*sum(1 for h in HOUSES if max(p[h],q[h])>=20); G=20*min(5,len(bonding))
    ep={h:max(0,p[h]-q[h]) for h in HOUSES}; eq={h:max(0,q[h]-p[h]) for h in HOUSES}
    f=sum(min(ep[a],eq[b])+min(ep[b],eq[a]) for a,b in [("Gryffindor","Ravenclaw"),("Slytherin","Hufflepuff"),("Gryffindor","Slytherin")]); F=min(100,1.5*f)
    score=max(0,min(100,round(0.45*max(S,C)+0.35*G+0.20*(100-F))))
    same=ai["primary"]==hu["primary"]; pp,qp=p[ai["primary"]],q[hu["primary"]]
    loyal=lambda s:s["dims"]["loyalty"]>=60 or s["dims"]["selective_loyalty"]>=60; explore=lambda s:s["dims"]["curiosity"]>=60 and s["dims"]["novelty"]>=50
    rules=[("高火花高摩擦型",F>=50 and G>=60),("镜像挑战型",same and ai["primary"] in ("Gryffindor","Slytherin") and pp>=45 and qp>=45),("慢热深连型",G>=80 and S<60 and months>=3),("一强一稳型",(pp>=55 and max(q.values())<=40) or (qp>=55 and max(p.values())<=40)),("温柔承托型",max(p["Hufflepuff"],q["Hufflepuff"])>=40 and not same and G>=60),("护短联盟型",loyal(ai) and loyal(hu)),("策略同盟型",p["Slytherin"]+q["Slytherin"]>=50),("行动推进型",p["Gryffindor"]+q["Gryffindor"]>=70),("脑力共创型",p["Ravenclaw"]>=30 and q["Ravenclaw"]>=30),("探索搭子型",explore(ai) and explore(hu)),("互补搭档型",not same and S<60 and C>=75 and F<40),("同频共振型",same and S>=75)]
    matched=[name for name,ok in rules if ok] or (["同频共振型"] if S>=60 else ["互补搭档型"])
    def conf(s):
        if s["contaminated"] or s["n_behaviors"]<5:return 0
        if s["blind"] and s["runs"]>=3 and s["n_behaviors"]>=8:return 2
        return 1
    hu_conf=0 if (not hu["blind"] or hu["n_behaviors"]<5) else (2 if hu["n_behaviors"]>=8 else 1)
    return {"S":round(S,1),"C":C,"G":G,"F":round(F,1),"compatibility":score,"primary_archetype":matched[0],"secondary_archetype":matched[1] if len(matched)>1 else None,"all_matched":matched,"confidence":["low","medium","high"][min(conf(ai),hu_conf)]}
def main():
    data=json.load(open(sys.argv[1],encoding="utf-8")); ai,hu=side(data["ai"]),side(data["human"]); print(json.dumps({"ai":ai,"human":hu,"pair":pair(ai,hu,data.get("bonding_behaviors",[]),data.get("relationship_months",0))},ensure_ascii=False,indent=2))
if __name__=="__main__": main()
