from __future__ import annotations
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path: sys.path.insert(0, str(ROOT))
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import engine

st.set_page_config(page_title="SkillLoop — Exchange what you know", page_icon="✳", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family:'DM Sans',sans-serif; }
.stApp { background:#F7F7FB; }
.block-container { padding-top:2.0rem; padding-bottom:3rem; max-width:1250px; }
[data-testid="stSidebar"] { background:#171725; }
[data-testid="stSidebar"] * { color:#F5F4FF !important; }
[data-testid="stSidebar"] [data-testid="stRadio"] label { padding:8px 10px; border-radius:10px; }
h1,h2,h3 { font-family:'Manrope',sans-serif !important; letter-spacing:-.035em; color:#191925; }
.eyebrow { color:#7569D9; text-transform:uppercase; letter-spacing:.14em; font-size:11px; font-weight:800; }
.hero { background:linear-gradient(120deg,#24223C 0%,#51458D 100%); padding:30px 34px; border-radius:22px; color:white; margin:4px 0 22px 0; }
.hero h1 { color:white !important; font-size:34px; margin:5px 0 8px 0; }
.hero p { color:#E2DFFF; margin:0; font-size:15px; }
.metric-card { background:white; border:1px solid #ECEBF3; border-radius:17px; padding:18px 20px; min-height:112px; box-shadow:0 4px 18px rgba(25,25,37,.035); }
.metric-label { color:#77768A; font-size:12px; font-weight:700; }
.metric-value { font-family:'Manrope'; color:#222137; font-size:29px; font-weight:800; margin-top:7px; }
.surface { background:white; border:1px solid #ECEBF3; border-radius:18px; padding:20px 22px; margin-bottom:14px; }
.pill { display:inline-block; background:#F0EEFF; color:#6356C7; border-radius:999px; padding:5px 10px; font-size:11px; font-weight:700; margin:3px 4px 3px 0; }
.muted { color:#77768A; font-size:13px; }
div.stButton > button { border-radius:11px; border:0; font-weight:700; padding:.58rem 1rem; }
.stTextInput input,.stSelectbox div[data-baseweb="select"],.stTextArea textarea { border-radius:10px; }
hr { border-color:#ECEBF3; }
[data-testid="stDataFrame"] { border:1px solid #ECEBF3; border-radius:12px; }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def boot():
    engine.ensure_engine()
    if not (engine.DATA / "students.csv").exists(): engine.initialise()
    if not (engine.DATA / "exchanges.csv").exists(): engine.initialise()
    return True

try:
    boot()
except Exception as exc:
    st.error("SkillLoop could not start its C++ engine.")
    st.code(str(exc))
    st.info("For local use, install a C++17 compiler (g++). Streamlit Cloud installs it from packages.txt.")
    st.stop()

def get_students():
    rows=engine.students()
    cols=["id","name","email","course","year","teaches","learns","availability","mode"]
    return pd.DataFrame(rows,columns=cols) if rows else pd.DataFrame(columns=cols)
def get_exchanges():
    rows=engine.exchanges(); cols=["id","requester_id","target_id","skill","status","created_at"]
    return pd.DataFrame(rows,columns=cols) if rows else pd.DataFrame(columns=cols)
def skill_tags(value):
    return [x.strip() for x in (value or "").split(",") if x.strip()]
def metric(label,value,caption=""):
    st.markdown(f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value">{value}</div><div class="muted">{caption}</div></div>',unsafe_allow_html=True)
def header(kicker,title,desc):
    st.markdown(f'<div class="eyebrow">{kicker}</div>',unsafe_allow_html=True)
    st.title(title); st.markdown(f'<p class="muted">{desc}</p>',unsafe_allow_html=True)
def show_tags(value):
    tags=[x for x in (value or "").split(";") if x]
    return "".join(f'<span class="pill">{t}</span>' for t in tags) or '<span class="muted">Not added yet</span>'

students=get_students(); exchanges=get_exchanges()
with st.sidebar:
    st.markdown("<div style='font-family:Manrope;font-size:25px;font-weight:800;letter-spacing:-1px'>✳ SkillLoop</div><div style='color:#AAA7C9;font-size:12px;margin:3px 0 22px'>CAMPUS SKILL EXCHANGE</div>",unsafe_allow_html=True)
    page=st.radio("NAVIGATION",["Overview","Discover","My Profile","Exchanges","Analytics"],label_visibility="collapsed")
    st.markdown("<br><div style='color:#AAA7C9;font-size:11px'>YOUR DEMO PROFILE</div>",unsafe_allow_html=True)
    if not students.empty:
        selected_id=st.selectbox("Signed in as",["NEW"]+students["id"].tolist(),index=1 if len(students) else 0,format_func=lambda x: "＋ Create new profile" if x=="NEW" else students.loc[students.id==x,"name"].iloc[0])
    else: selected_id=None
    st.markdown("<br><div style='color:#AAA7C9;font-size:11px'>BUILT WITH C++17 · STREAMLIT</div>",unsafe_allow_html=True)

current=students[students.id==selected_id].iloc[0] if selected_id and selected_id!="NEW" and not students.empty and not students[students.id==selected_id].empty else None
if page=="Overview":
    st.markdown('<div class="hero"><div style="font-size:12px;letter-spacing:2px;font-weight:800;color:#C7C0FF">LEARN TOGETHER. GROW TOGETHER.</div><h1>Trade your skills.<br>Unlock your potential.</h1><p>Find the people who know what you want to learn — and want what you know.</p></div>',unsafe_allow_html=True)
    if current is not None: st.markdown(f"### {current['name']}, your next skill exchange starts here.")
    a,b,c,d=st.columns(4)
    with a: metric("COMMUNITY MEMBERS",len(students),"Students on SkillLoop")
    with b: metric("SKILLS OFFERED",len(set(x for v in students.teaches for x in v.split(';') if x)),"Unique skills shared")
    with c: metric("EXCHANGE REQUESTS",len(exchanges),"Across the community")
    with d: metric("ACCEPTED",int((exchanges.status=="Accepted").sum()) if not exchanges.empty else 0,"Successful connections")
    st.markdown("### Your skill snapshot")
    if current is not None:
        x,y=st.columns(2)
        with x:
            st.markdown('<div class="surface"><b>✦ Skills I can teach</b><br><br>'+show_tags(current.teaches)+'</div>',unsafe_allow_html=True)
        with y:
            st.markdown('<div class="surface"><b>◎ Skills I want to learn</b><br><br>'+show_tags(current.learns)+'</div>',unsafe_allow_html=True)
    st.markdown("### How SkillLoop works")
    x,y,z=st.columns(3)
    x.markdown('<div class="surface"><div class="eyebrow">01 / SHARE</div><h3>Offer a skill</h3><p class="muted">Tell the community what you can teach with confidence.</p></div>',unsafe_allow_html=True)
    y.markdown('<div class="surface"><div class="eyebrow">02 / DISCOVER</div><h3>Find your match</h3><p class="muted">Our C++ matching engine finds reciprocal learning opportunities.</p></div>',unsafe_allow_html=True)
    z.markdown('<div class="surface"><div class="eyebrow">03 / EXCHANGE</div><h3>Learn together</h3><p class="muted">Send a request, connect and exchange knowledge.</p></div>',unsafe_allow_html=True)

elif page=="Discover":
    header("FIND YOUR PEOPLE","Discover your next exchange","Every match is based on a two-way skill fit, not just shared interests.")
    if current is None: st.warning("Add a student profile to start discovering matches.")
    else:
        st.markdown(f"<div class='surface'><b>You're browsing as {current['name']}</b><br><span class='muted'>Teaching: {current['teaches'].replace(';', ', ')} · Learning: {current['learns'].replace(';', ', ')}</span></div>",unsafe_allow_html=True)
        matches=engine.matches(selected_id)
        if not matches: st.info("No reciprocal matches yet. Add more skills to your profile or invite classmates to join.")
        else:
            for row in matches:
                sid,name,skill,score,reason=row
                target=students[students.id==sid].iloc[0]
                with st.container(border=True):
                    left,right=st.columns([4,1])
                    with left:
                        st.markdown(f"### {name}  <span class='pill'>{target.course}</span>",unsafe_allow_html=True)
                        st.markdown(f"**Two-way exchange:** {skill}")
                        st.caption(f"{target.availability} · {target['mode']} · {reason}")
                    with right:
                        st.metric("COMPATIBILITY",f"{float(score):.0f}%")
                        if st.button("Request exchange",key="req_"+sid,use_container_width=True):
                            requested=skill.split(" ↔ ")[0]
                            engine.create_exchange(selected_id,sid,requested)
                            st.success(f"Request sent to {name}!"); st.rerun()

elif page=="My Profile":
    header("YOUR SPACE","Build your learning profile","The clearer your profile, the better your matches.")
    with st.form("profile_form",clear_on_submit=False):
        c1,c2=st.columns(2)
        with c1:
            name=st.text_input("Full name",value=current["name"] if current is not None else "")
            email=st.text_input("Email",value=current.email if current is not None else "")
            course=st.text_input("Course / department",value=current.course if current is not None else "")
            year=st.selectbox("Year of study",["1","2","3","4"],index=(int(current.year)-1 if current is not None and current.year.isdigit() and 1<=int(current.year)<=4 else 0),format_func=lambda x:f"Year {x}")
        with c2:
            teaches=st.text_area("Skills you can teach (comma separated)",value=current.teaches.replace(";",", ") if current is not None else "",placeholder="Python, Public Speaking, UI Design")
            learns=st.text_area("Skills you want to learn (comma separated)",value=current.learns.replace(";",", ") if current is not None else "",placeholder="C++, Graphic Design")
            availability=st.selectbox("Availability",["Weekday evenings","Weekends","Weekday mornings","Flexible"],index=["Weekday evenings","Weekends","Weekday mornings","Flexible"].index(current.availability) if current is not None and current.availability in ["Weekday evenings","Weekends","Weekday mornings","Flexible"] else 0)
            mode=st.selectbox("Preferred learning mode",["Online","Offline","Hybrid"],index=["Online","Offline","Hybrid"].index(current['mode']) if current is not None and current['mode'] in ["Online","Offline","Hybrid"] else 0)
        submitted=st.form_submit_button("Save profile",type="primary",use_container_width=True)
    if submitted:
        if not name.strip() or not email.strip() or not course.strip() or not skill_tags(teaches) or not skill_tags(learns): st.error("Please complete your name, email, course, and both skill lists.")
        elif current is not None:
            engine.update_student(selected_id,name.strip(),email.strip(),course.strip(),year,skill_tags(teaches),skill_tags(learns),availability,mode)
            st.success("Profile updated!"); st.rerun()
        else:
            new_id="S"+str(100+len(students)+1)
            engine.add_student(new_id,name.strip(),email.strip(),course.strip(),year,skill_tags(teaches),skill_tags(learns),availability,mode)
            st.success("Profile created!"); st.rerun()
    with st.expander("Create an additional student profile"):
        st.caption("For this academic demo, each new submission creates a new profile record.")

elif page=="Exchanges":
    header("KEEP IT MOVING","My exchanges","Track requests and manage the learning connections you've started.")
    if exchanges.empty: st.info("No exchange requests yet. Head to Discover and request your first exchange.")
    else:
        lookup={r.id:r.name for _,r in students.iterrows()}
        mine=exchanges[(exchanges.requester_id==selected_id)|(exchanges.target_id==selected_id)] if selected_id else exchanges
        for _,e in mine.iterrows():
            other=e.target_id if e.requester_id==selected_id else e.requester_id
            with st.container(border=True):
                c1,c2,c3=st.columns([3,1,1])
                c1.markdown(f"**{e.skill}**<br><span class='muted'>{'To' if e.requester_id==selected_id else 'From'} {lookup.get(other,other)} · {e.created_at}</span>",unsafe_allow_html=True)
                c2.write(e.status)
                if e.target_id==selected_id and e.status=="Pending":
                    with c3:
                        if st.button("Accept",key="accept_"+e.id): engine.update_exchange(e.id,"Accepted"); st.rerun()
                        if st.button("Decline",key="decline_"+e.id): engine.update_exchange(e.id,"Declined"); st.rerun()
                elif e.requester_id==selected_id and e.status=="Pending": c3.caption("Awaiting response")

elif page=="Analytics":
    header("COMMUNITY INSIGHTS","Skills in motion","A live snapshot of the knowledge being shared across your campus.")
    if students.empty: st.info("Add students to generate analytics.")
    else:
        offered=[s.strip() for cell in students.teaches for s in cell.split(";") if s.strip()]
        wanted=[s.strip() for cell in students.learns for s in cell.split(";") if s.strip()]
        supply=pd.Series(offered).value_counts().rename_axis("Skill").reset_index(name="Students offering")
        demand=pd.Series(wanted).value_counts().rename_axis("Skill").reset_index(name="Students seeking")
        merged=supply.merge(demand,on="Skill",how="outer").fillna(0)
        merged["Gap"]=merged["Students seeking"]-merged["Students offering"]
        c1,c2=st.columns(2)
        with c1:
            st.markdown("#### Most offered skills")
            fig,ax=plt.subplots(figsize=(6,3.5)); top=supply.head(7).sort_values("Students offering"); ax.barh(top.Skill,top["Students offering"],color="#7669D8"); ax.set_xlabel("Students"); ax.spines[['top','right','left']].set_visible(False); fig.tight_layout(); st.pyplot(fig); plt.close(fig)
        with c2:
            st.markdown("#### Most wanted skills")
            fig,ax=plt.subplots(figsize=(6,3.5)); top=demand.head(7).sort_values("Students seeking"); ax.barh(top.Skill,top["Students seeking"],color="#B6A9F4"); ax.set_xlabel("Students"); ax.spines[['top','right','left']].set_visible(False); fig.tight_layout(); st.pyplot(fig); plt.close(fig)
        st.markdown("#### Campus skill gaps")
        st.dataframe(merged.sort_values("Gap",ascending=False),use_container_width=True,hide_index=True)
        st.download_button("Download analytics CSV",merged.to_csv(index=False).encode(),"skillloop_analytics.csv","text/csv")

st.markdown("<br><div style='text-align:center;color:#9A99A8;font-size:11px'>SKILLLOOP · A C++ OBJECT-ORIENTED PROGRAMMING PROJECT</div>",unsafe_allow_html=True)
