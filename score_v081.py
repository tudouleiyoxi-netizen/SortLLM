#!/usr/bin/env python3
"""SortLLM v0.8.1 deterministic scorer. Usage: python3 score_v081.py input.json"""
import json, re, sys, os, math
HOUSES=["Gryffindor","Ravenclaw","Hufflepuff","Slytherin"]
SPEC=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"sortllm_pairing_ritual_v081.json"),encoding="utf-8"))
ITEMS={it["id"]:it["options"] for it in SPEC["questionnaire"]["items"]}; POINTS=SPEC["questionnaire"]["rank_points"]
DIMS=sorted({d for opts in ITEMS.values() for o in opts.values() for d in o["dims"]})
ANCHORS=SPEC["behavior_evidence"]["anchors"]
def parse_rank(s):
    letters=re.findall(r"[ABCD]",s.upper())
    if sorted(letters)!=["A","B","C","D"]: raise ValueError(f"bad ranking: {s!r}")
    return letters
def questionnaire(runs):
    house={h:0.0 for h in HOUSES}; dim={d:0.0 for d in DIMS}; dim_max={d:0.0 for d in DIMS}
    for run in runs:
        if set(run)!=set(ITEMS): raise ValueError("each run must answer Q1-Q12")
        for qid,ranking in run.items():
            for pos,letter in enumerate(parse_rank(ranking)):
                opt=ITEMS[qid][letter]; house[opt["house"]]+=POINTS[pos]
                for d in opt["dims"]: dim[d]+=POINTS[pos]; dim_max[d]+=POINTS[0]
    total=sum(house.values())
    return ({h:100*v/total for h,v in house.items()},{d:round(100*dim[d]/dim_max[d],1) for d in DIMS})
def valid_behavior(item):
    if item.get("house") not in HOUSES: return False
    anchor=item.get("anchor","")
    return anchor in ANCHORS[item["house"]] and bool(item.get("note")) and bool(item.get("source"))
def behavior(items):
    valid=[b for b in items if valid_behavior(b)]; n=len(valid); counts={h:sum(1 for b in valid if b["house"]==h) for h in HOUSES}
    return {h:(counts[h]+0.5)/(n+2)*100 for h in HOUSES},n,valid
def side(data):
    q,dims=questionnaire(data["runs"]); b,n,valid=behavior(data.get("behaviors",[])); wq,wb=((0.6,0.4) if n>=5 else (0.8,0.2))
    final={h:wq*q[h]+wb*b[h] for h in HOUSES}; ranked=sorted(HOUSES,key=lambda h:-final[h])
    return {"final":{h:round(final[h],1) for h in HOUSES},"questionnaire":{h:round(q[h],1) for h in HOUSES},"dims":dims,"primary":ranked[0],"second":ranked[1],"n_behaviors":n,"valid_behaviors":valid,"runs":len(data["runs"]),"contaminated":data.get("contaminated",False),"blind":data.get("blind",True)}
def axis_positions(s):
    d=s["dims"]
    return {"pace":d["action"]-d["analysis"],"confrontation":d["directness"]-d["cooperation"],"partiality":d["selective_loyalty"]-d["fairness"],"method":d["strategy"]-d["principle"]}
def valid_bonding(items):
    out=[]
    for x in items[:5]:
        if isinstance(x,dict) and x.get("event") and x.get("ai_action") and x.get("human_action"): out.append(x)
    return out
def pair(ai,hu,bonding,months):
    p,q=ai["final"],hu["final"]; S=100-0.5*sum(abs(p[h]-q[h]) for h in HOUSES); C=25*sum(1 for h in HOUSES if max(p[h],q[h])>=20)
    bonds=valid_bonding(bonding); G=round(100*(1-(0.75**len(bonds))))
    ap,aq=axis_positions(ai),axis_positions(hu); F=round(sum(abs(ap[k]-aq[k]) for k in ap)/len(ap)/2)
    fit=0.7*S+0.3*C; score=max(0,min(100,round(0.45*fit+0.35*G+0.20*(100-F))))
    same=ai["primary"]==hu["primary"]; pp,qp=p[ai["primary"]],q[hu["primary"]]
    loyal=lambda s:s["dims"]["loyalty"]>=60 or s["dims"]["selective_loyalty"]>=60; explore=lambda s:s["dims"]["curiosity"]>=60 and s["dims"]["novelty"]>=50
    rules=[("高火花高摩擦型",F>=50 and G>=55),("镜像挑战型",same and ai["primary"] in ("Gryffindor","Slytherin") and pp>=45 and qp>=45),("慢热深连型",G>=65 and S<60 and months>=3),("一强一稳型",(pp>=55 and max(q.values())<=40) or (qp>=55 and max(p.values())<=40)),("温柔承托型",max(p["Hufflepuff"],q["Hufflepuff"])>=40 and not same and G>=55),("护短联盟型",loyal(ai) and loyal(hu)),("策略同盟型",p["Slytherin"]+q["Slytherin"]>=50),("行动推进型",p["Gryffindor"]+q["Gryffindor"]>=70),("脑力共创型",p["Ravenclaw"]>=30 and q["Ravenclaw"]>=30),("探索搭子型",explore(ai) and explore(hu)),("互补搭档型",not same and S<60 and C>=75 and F<40),("同频共振型",same and S>=75)]
    matched=[name for name,ok in rules if ok] or (["同频共振型"] if S>=60 else ["互补搭档型"])
    low=(not ai["blind"] or not hu["blind"] or ai["contaminated"] or hu["contaminated"] or ai["n_behaviors"]<5 or hu["n_behaviors"]<5)
    high=(not low and ai["runs"]>=3 and ai["n_behaviors"]>=8 and hu["n_behaviors"]>=8)
    confidence="low" if low else ("high" if high else "medium")
    return {"S":round(S,1),"C":C,"G":G,"F":F,"fit":round(fit,1),"compatibility":score,"friction_axes_ai":ap,"friction_axes_human":aq,"primary_archetype":matched[0],"secondary_archetype":matched[1] if len(matched)>1 else None,"all_matched":matched,"confidence":confidence,"valid_bonding_events":bonds}
def main():
    data=json.load(open(sys.argv[1],encoding="utf-8")); ai,hu=side(data["ai"]),side(data["human"]); out={"version":"0.8.1","ai":ai,"human":hu,"pair":pair(ai,hu,data.get("bonding_behaviors",[]),data.get("relationship_months",0))}; print(json.dumps(out,ensure_ascii=False,indent=2))
if __name__=="__main__": main()
