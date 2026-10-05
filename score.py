#!/usr/bin/env python3
"""SortLLM v0.9 deterministic scorer. Usage: python3 score.py input.json"""
import json, os, sys

HOUSES=["Gryffindor","Ravenclaw","Hufflepuff","Slytherin"]
ROOT=os.path.dirname(os.path.abspath(__file__))
SPEC=json.load(open(os.path.join(ROOT,"sortllm_pairing_ritual_v09.json"),encoding="utf-8"))
ITEMS={it["id"]:it["options"] for it in SPEC["questionnaire"]["items"]}
D2H=SPEC["dimension_to_house"]
DIMS=sorted(D2H)
PSEUDO=float(SPEC["questionnaire"].get("house_pseudocount",0.5))

def parse_choice(x):
    s=str(x).strip().upper()
    if s not in "ABCD" or len(s)!=1:
        raise ValueError(f"bad single-choice answer: {x!r}")
    return s

def questionnaire(runs):
    if not runs:
        raise ValueError("at least one questionnaire run is required")
    house_counts={h:0.0 for h in HOUSES}
    dim_hits={d:0.0 for d in DIMS}
    dim_opps={d:0.0 for d in DIMS}
    for run in runs:
        if set(run)!=set(ITEMS):
            raise ValueError("each run must answer Q1-Q12 exactly once")
        for qid,opts in ITEMS.items():
            for o in opts.values():
                for d in o["dims"]:
                    dim_opps[d]+=1
            letter=parse_choice(run[qid])
            opt=opts[letter]
            house_counts[opt["house"]]+=1
            for d in opt["dims"]:
                dim_hits[d]+=1
    total=sum(house_counts.values())+PSEUDO*len(HOUSES)
    houses={h:100*(house_counts[h]+PSEUDO)/total for h in HOUSES}
    dims={d:(100*dim_hits[d]/dim_opps[d] if dim_opps[d] else 0.0) for d in DIMS}
    return houses,dims

def valid_behavior(item):
    if not isinstance(item,dict) or not item.get("note") or not item.get("source"):
        return False
    dims=item.get("dimensions")
    if not isinstance(dims,list) or not (1<=len(dims)<=2) or len(set(dims))!=len(dims):
        return False
    if any(d not in D2H for d in dims):
        return False
    if item.get("instructed",False):
        return False
    if item.get("self_description",False) and not item.get("corroborated",False):
        return False
    return True

def behavior(items):
    valid=[x for x in items if valid_behavior(x)]
    house_counts={h:0.0 for h in HOUSES}
    dim_counts={d:0.0 for d in DIMS}
    total_tags=0
    for x in valid:
        for d in x["dimensions"]:
            dim_counts[d]+=1
            house_counts[D2H[d]]+=1
            total_tags+=1
    htotal=total_tags+PSEUDO*len(HOUSES)
    houses={h:100*(house_counts[h]+PSEUDO)/htotal for h in HOUSES} if htotal else {h:25.0 for h in HOUSES}
    dims={d:(100*dim_counts[d]/total_tags if total_tags else 0.0) for d in DIMS}
    return houses,dims,len(valid),valid

def side(data):
    qh,qd=questionnaire(data["runs"])
    bh,bd,n,valid=behavior(data.get("behaviors",[]))
    wq,wb=((0.6,0.4) if n>=5 else (0.8,0.2))
    final={h:wq*qh[h]+wb*bh[h] for h in HOUSES}
    dims={d:wq*qd[d]+wb*bd[d] for d in DIMS}
    ranked=sorted(HOUSES,key=lambda h:(-final[h],h))
    return {
        "final":{h:round(final[h],1) for h in HOUSES},
        "questionnaire":{h:round(qh[h],1) for h in HOUSES},
        "behavior":{h:round(bh[h],1) for h in HOUSES},
        "dims":{d:round(dims[d],1) for d in DIMS},
        "primary":ranked[0],"second":ranked[1],
        "n_behaviors":n,"valid_behaviors":valid,"runs":len(data["runs"]),
        "contaminated":bool(data.get("contaminated",False)),"blind":bool(data.get("blind",True))
    }

def axis_positions(s):
    d=s["dims"]
    return {
        "pace":d["action"]-d["analysis"],
        "confrontation":d["directness"]-d["cooperation"],
        "partiality":d["selective_loyalty"]-d["fairness"],
        "method":d["strategy"]-d["principle"]
    }

def valid_bonding(items):
    out=[]
    for x in items[:5]:
        if isinstance(x,dict) and x.get("event") and x.get("ai_action") and x.get("human_action"):
            out.append(x)
    return out

def pair(ai,hu,bonding,months):
    p,q=ai["final"],hu["final"]
    S=100-0.5*sum(abs(p[h]-q[h]) for h in HOUSES)
    C=25*sum(1 for h in HOUSES if max(p[h],q[h])>=20)
    bonds=valid_bonding(bonding)
    G=round(100*(1-(0.75**len(bonds))))
    ap,aq=axis_positions(ai),axis_positions(hu)
    F=round(sum(abs(ap[k]-aq[k]) for k in ap)/len(ap)/2)
    fit=0.7*S+0.3*C
    score=max(0,min(100,round(0.45*fit+0.35*G+0.20*(100-F))))
    same=ai["primary"]==hu["primary"]
    pp,qp=p[ai["primary"]],q[hu["primary"]]
    loyal=lambda s:s["dims"]["loyalty"]>=60 or s["dims"]["selective_loyalty"]>=60
    explore=lambda s:s["dims"]["curiosity"]>=60 and s["dims"]["novelty"]>=50
    rules=[
        ("高火花高摩擦型",F>=50 and G>=55),
        ("镜像挑战型",same and ai["primary"] in ("Gryffindor","Slytherin") and pp>=45 and qp>=45),
        ("慢热深连型",G>=65 and S<60 and months>=3),
        ("一强一稳型",(pp>=55 and max(q.values())<=40) or (qp>=55 and max(p.values())<=40)),
        ("温柔承托型",max(p["Hufflepuff"],q["Hufflepuff"])>=40 and not same and G>=55),
        ("护短联盟型",loyal(ai) and loyal(hu)),
        ("策略同盟型",p["Slytherin"]+q["Slytherin"]>=50),
        ("行动推进型",p["Gryffindor"]+q["Gryffindor"]>=70),
        ("脑力共创型",p["Ravenclaw"]>=30 and q["Ravenclaw"]>=30),
        ("探索搭子型",explore(ai) and explore(hu)),
        ("互补搭档型",not same and S<60 and C>=75 and F<40),
        ("同频共振型",same and S>=75)
    ]
    matched=[name for name,ok in rules if ok] or (["同频共振型"] if S>=60 else ["互补搭档型"])
    low=(not ai["blind"] or not hu["blind"] or ai["contaminated"] or hu["contaminated"] or ai["n_behaviors"]<5 or hu["n_behaviors"]<5)
    high=(not low and ai["runs"]>=3 and ai["n_behaviors"]>=8 and hu["n_behaviors"]>=8)
    confidence="low" if low else ("high" if high else "medium")
    return {
        "S":round(S,1),"C":C,"G":G,"F":F,"fit":round(fit,1),"compatibility":score,
        "friction_axes_ai":{k:round(v,1) for k,v in ap.items()},
        "friction_axes_human":{k:round(v,1) for k,v in aq.items()},
        "primary_archetype":matched[0],"secondary_archetype":matched[1] if len(matched)>1 else None,
        "all_matched":matched,"confidence":confidence,"valid_bonding_events":bonds
    }

def main():
    if len(sys.argv)!=2:
        raise SystemExit("usage: python3 score.py input.json")
    data=json.load(open(sys.argv[1],encoding="utf-8"))
    ai,hu=side(data["ai"]),side(data["human"])
    out={"version":"0.9","ai":ai,"human":hu,"pair":pair(ai,hu,data.get("bonding_behaviors",[]),data.get("relationship_months",0))}
    print(json.dumps(out,ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
