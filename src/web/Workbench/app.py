import streamlit as st
import pandas as pd, hashlib, uuid
from datetime import datetime
st.set_page_config(page_title="Orbyte | AI Customer Workbench",page_icon="✦",layout="wide")
if "messages" not in st.session_state:
 st.session_state.messages=[
 {"id":"MSG-2401","time":"20:54","channel":"WhatsApp","account":"Northstar Trading","sender":"Mia Chen","body":"The shipment for PO-8842 still hasn't arrived. Our warehouse closes at 18:00 tomorrow. Can you confirm the delivery status tonight?","importance":92,"urgency":96,"risk":"Delivery deadline","reason":"Explicit request for confirmation tonight; the warehouse closes tomorrow, affecting delivery.","status":"Pending"},
 {"id":"MSG-2402","time":"20:31","channel":"Email","account":"BluePeak Retail","sender":"Daniel Wong","body":"Could you send the latest product catalogue and the updated wholesale price list for Q4?","importance":71,"urgency":48,"risk":"External document review","reason":"Product catalog and pricing require version and sharing permission checks.","status":"Pending"},
 {"id":"MSG-2403","time":"19:48","channel":"Discord","account":"Cedar Labs","sender":"Evan Li","body":"We noticed an unexpected change in the billing destination. Please pause the transfer until we verify this with your finance team.","importance":97,"urgency":93,"risk":"Payment/fraud risk","reason":"Unusual change to payment destination; customer requested a pause and verification.","status":"Risk review"},
 {"id":"MSG-2404","time":"18:20","channel":"WhatsApp","account":"BluePeak Retail","sender":"Daniel Wong","body":"Thanks for the quick turnaround last week. The samples look good.","importance":39,"urgency":18,"risk":"No clear risk signal","reason":"General feedback with no explicit deadline or high-impact issue.","status":"Viewed"},
 {"id":"MSG-2405","time":"17:56","channel":"Email","account":"Northstar Trading","sender":"Mia Chen","body":"Please confirm whether the revised invoice includes the agreed shipping credit of USD 1,250.","importance":84,"urgency":72,"risk":"Invoice/amount verification","reason":"Specific amount and invoice terms require checking against approved records.","status":"Pending"},
 {"id":"MSG-2406","time":"16:43","channel":"WhatsApp","account":"Harborline Supply","sender":"Sofia Tan","body":"No rush—just checking if the onboarding guide is available when you have a chance.","importance":28,"urgency":12,"risk":"No clear risk signal","reason":"Customer said there is no rush; this is a routine information request.","status":"Pending"}]
if "accounts" not in st.session_state:
 st.session_state.accounts={
 "Northstar Trading":{"industry":"Wholesale trade","stage":"Established","value":88,"growth":72,"risk":"Low","attention":"High attention","facts":"Order history is stable; there are current delivery deadline and invoice verification items."},
 "BluePeak Retail":{"industry":"Retail","stage":"Growing","value":71,"growth":84,"risk":"Low","attention":"Normal attention","facts":"Recently requested the Q4 product catalog and wholesale price list."},
 "Cedar Labs":{"industry":"Technology / Labs","stage":"Active","value":64,"growth":69,"risk":"Review needed","attention":"Normal attention","facts":"An unusual payment destination change was detected. Account value must not lower risk priority."},
 "Harborline Supply":{"industry":"Supply chain","stage":"Early-stage","value":43,"growth":51,"risk":"Unknown","attention":"Low attention","facts":"The current message is a low-urgency information request."}}
if "audit" not in st.session_state: st.session_state.audit=[{"Time":"Startup","Event":"Demo data loaded","Object":"System","Result":"Local simulation only"}]
if "tasks" not in st.session_state: st.session_state.tasks={}
if "drafts" not in st.session_state: st.session_state.drafts={}
def log(event,obj,result):
 st.session_state.audit.insert(0,{"Time":datetime.now().strftime("%H:%M:%S"),"Event":event,"Object":obj,"Result":result})
def digest(body,recipient,channel,attachment):
 return hashlib.sha256("|".join([body,recipient,channel,attachment]).encode()).hexdigest()
def box(label,value,sub):
 st.markdown(f'<div style="border:1px solid #e5eaf1;border-radius:14px;padding:16px;background:white"><div style="color:#667085;font-size:12px">{label}</div><div style="font-size:27px;font-weight:700;color:#172554">{value}</div><div style="color:#667085;font-size:11px">{sub}</div></div>',unsafe_allow_html=True)
st.markdown("""<style>.block-container{padding-top:1.2rem;max-width:1500px}.hero{padding:24px 28px;border-radius:18px;color:white;background:linear-gradient(120deg,#172554,#4058a6);margin-bottom:18px}.hero h1{color:white;margin:0}.hero p{color:#dbe5ff;margin:5px 0 0}.muted{color:#667085;font-size:12px}</style>""",unsafe_allow_html=True)
st.sidebar.markdown("# ✦ ORBYTE")
st.sidebar.caption("AI Business Customer Messaging Workbench")
page=st.sidebar.radio("Workspace",["Overview","Message Inbox","Customer Accounts","AI Reply Assistant","Safe Send Simulation","Model & Tests","Audit Log"])
st.sidebar.divider(); st.sidebar.success("Local Demo Mode")
st.sidebar.caption("No live channel connection · No external AI API · Nothing is actually sent")
M=st.session_state.messages; A=st.session_state.accounts
if page=="Overview":
 st.markdown('<div class="hero"><h1>Customer messages. Clear decisions. Safer actions.</h1><p>Unified channels · AI priority scoring · Personal alerts · Human-reviewed replies</p></div>',unsafe_allow_html=True)
 c=st.columns(4)
 for col,l,v,s in zip(c,["Demo Messages","High Urgency","Open Items","Customer Accounts"],[len(M),sum(m["urgency"]>=80 for m in M),sum(m["status"] in ["Pending","Risk review"] for m in M),len(A)],["3 simulated channels","Urgency ≥ 80","Includes risk reviews","Personal alert settings are private"]):
  with col: box(l,v,s)
 st.write(""); left,right=st.columns([1.3,1])
 with left:
  st.subheader("Priority Queue")
  for m in sorted(M,key=lambda x:(x["urgency"]>=80,x["importance"]),reverse=True)[:5]:
   with st.container(border=True):
    st.markdown(f"**{'🔴' if m['urgency']>=85 else '🟠' if m['urgency']>=60 else '🟢'} {m['account']} · {m['sender']}**")
    st.caption(f"{m['channel']} · {m['time']} · {m['risk']}")
    st.write(m["body"]); st.write(f"Importance **{m['importance']}** / 100　|　Urgency **{m['urgency']}** / 100")
 with right:
  st.subheader("Accounts & Risk")
  st.dataframe(pd.DataFrame([{"Customer":k,"Attention level":v["attention"],"Account Score":v["value"],"Payment Risk":v["risk"]} for k,v in A.items()]),hide_index=True,use_container_width=True)
  st.info("Long-term account value never overrides message urgency or risk alerts.")
elif page=="Message Inbox":
 st.header("Message Inbox"); st.caption("Demo scores validate the interface and workflow; they are not production model predictions.")
 c=st.columns(3)
 with c[0]: channel=st.selectbox("Channel",["All","WhatsApp","Email","Discord"])
 with c[1]: urgency=st.selectbox("Urgency",["All","High ≥80","Medium 50–79","Low <50"])
 with c[2]: query=st.text_input("Search accounts or messages")
 filtered=[m for m in M if (channel=="All" or m["channel"]==channel) and (urgency=="All" or (urgency=="High ≥80" and m["urgency"]>=80) or (urgency=="Medium 50–79" and 50<=m["urgency"]<80) or (urgency=="Low <50" and m["urgency"]<50)) and (not query or query.lower() in (m["account"]+m["body"]+m["sender"]).lower())]
 left,right=st.columns([1,1.3])
 with left:
  for m in sorted(filtered,key=lambda x:x["urgency"],reverse=True):
   with st.container(border=True):
    st.markdown(f"**{m['account']}** · {m['channel']} · {m['time']}")
    st.write(m["body"][:140])
    st.caption(f"Importance {m['importance']} · Urgency {m['urgency']} · {m['status']}")
    if st.button("View details",key="view_"+m["id"]): st.session_state.selected=m["id"]
 with right:
  ids=[m["id"] for m in filtered]
  if not ids: st.info("No messages match these filters.")
  else:
   default=st.session_state.get("selected",ids[0]); m=next((x for x in filtered if x["id"]==default),filtered[0])
   st.subheader(m["account"]+" · "+m["sender"]); st.caption(m["id"]+" · "+m["channel"])
   st.markdown(f"> {m['body']}")
   x,y=st.columns(2)
   with x: st.metric("AI Importance (Demo)",str(m["importance"])+"/100")
   with y: st.metric("AI Urgency (Demo)",str(m["urgency"])+"/100")
   st.warning("Risk: "+m["risk"]); st.write("**Reasoning: ** "+m["reason"])
   st.write("**Suggested action: Verify business facts first; send high-risk items for human review. Model scores do not authorize sending or payment.** Verify business facts first; send high-risk items for human review. Model scores do not authorize sending or payment.")
   if st.button("Mark as viewed",key="mark_"+m["id"]): m["status"]="Viewed"; log("Message status updated",m["id"],"Viewed"); st.rerun()
elif page=="Customer Accounts":
 st.header("Customer Accounts"); st.caption("Personal attention level is a work preference, not an AI assessment of customer value.")
 name=st.selectbox("Select an account",list(A)); a=A[name]
 c=st.columns(4)
 for col,l,v,s in zip(c,["Account Score (Demo)","Growth Potential (Demo)","Payment Risk","Personal Attention"],[f"{a['value']}/100",f"{a['growth']}/100",a["risk"],a["attention"]],[a["industry"],a["stage"],"Evidence verification required","This demo user only"]):
  with col: box(l,v,s)
 left,right=st.columns(2)
 with left:
  st.subheader("Account Overview"); st.write("**Industry:**",a["industry"]); st.write("**Relationship Stage:**",a["stage"]); st.write(a["facts"])
  rel=[m for m in M if m["account"]==name]
  st.subheader("Related Messages"); st.dataframe(pd.DataFrame([{"Time":m["time"],"Channel":m["channel"],"Importance":m["importance"],"Urgency":m["urgency"],"Risk":m["risk"]} for m in rel]),hide_index=True,use_container_width=True)
 with right:
  st.subheader("Personal Attention Settings")
  level=st.radio("Attention level",["High attention","Normal attention","Low attention"],index=["High attention","Normal attention","Low attention"].index(a["attention"]),key="lvl_"+name)
  sound=st.selectbox("Sound",["Follow level","Prominent alert","Standard alert","Subtle / silent"],key="snd_"+name)
  visual=st.selectbox("Visual marker",["Automatic","Star","Blue dot","No extra marker"],key="vis_"+name)
  quiet=st.checkbox("Respect quiet hours 22:00–08:00",value=True,key="q_"+name)
  if st.button("Save personal settings",type="primary"):
   old=a["attention"]; a["attention"]=level; log("Personal alert settings changed",name,f"{old} → {level}; Sound={sound}; Visual={visual}; Quiet hours={quiet}")
   st.success("Saved to this demo session. This does not change AI scores or share settings with the team.")
  st.info("Changes in long-term account scores notify the user but do not change manual attention settings.")
elif page=="AI Reply Assistant":
 st.header("AI Reply & Knowledge Assistant"); st.caption("Uses local demo templates; no external AI API is called.")
 mid=st.selectbox("Select a message",[m["id"] for m in M]); m=next(x for x in M if x["id"]==mid)
 st.write(f"Customer:**{m['account']}** · Channel:{m['channel']}"); st.markdown("> "+m["body"])
 knowledge={
 "Northstar Trading":"Confirm order status in the order system; check invoice credits against approved terms. No real order-system data is available in this demo.",
 "BluePeak Retail":"Verify versions and sharing permissions before sending the product catalog or Q4 wholesale price list externally.",
 "Cedar Labs":"Pause actions after an unusual payment destination change and verify it with a trusted internal finance contact.",
 "Harborline Supply":"The onboarding guide can be shared after verifying its version and external sharing approval."}
 st.info("Retrieved demo knowledge:"+knowledge[m["account"]])
 defaults={
 "MSG-2401":"Hi Mia, thanks for flagging this. I’m checking the latest status for PO-8842 with our operations team. I’ll confirm the verified delivery status and next steps as soon as I have an update.",
 "MSG-2402":"Hi Daniel, happy to help. I’ll verify the latest approved Q4 catalogue and wholesale price list, including document versions and sharing permissions, before sending them over.",
 "MSG-2403":"Hi Evan, thank you for alerting us. We will pause any action related to the changed billing destination while finance verifies the request through an established contact channel.",
 "MSG-2404":"Hi Daniel, glad to hear the samples look good. Thanks for the feedback — we’ll be happy to help with next steps when you’re ready.",
 "MSG-2405":"Hi Mia, I’ll compare the revised invoice against the approved shipping-credit terms and confirm the amount once it has been verified.",
 "MSG-2406":"Hi Sofia, I’ll confirm the latest onboarding guide version and share it once I’ve verified that it is approved for external distribution."}
 if mid not in st.session_state.drafts: st.session_state.drafts[mid]=defaults[mid]
 body=st.text_area("Reply draft (editable)",value=st.session_state.drafts[mid],height=150,key="draft_"+mid); st.session_state.drafts[mid]=body
 recipient=st.text_input("Recipient",value=m["sender"],key="to_"+mid)
 attachment=st.selectbox("Attachment option",["No attachment","Q4 Product Catalog v3.2","Wholesale Price List v2026-Q4","Order Status Summary (Internal)","Contract Draft (Sensitive)"],key="att_"+mid)
 if attachment=="Contract Draft (Sensitive)": st.error("Sensitive attachment: the demo policy blocks sending.")
 st.write("Before sending, a person must review the message, recipient, channel, attachment version, and external sharing permissions.")
 if st.button("Save draft"):
  log("Reply draft saved",mid,"Saved locally; not sent"); st.success("Draft saved.")
 if st.button("Create review task",type="primary",disabled=not recipient.strip()):
  tid="SEND-"+uuid.uuid4().hex[:8].upper(); h=digest(body,recipient,m["channel"],attachment)
  st.session_state.tasks[tid]={"id":tid,"mid":mid,"body":body,"recipient":recipient,"channel":m["channel"],"attachment":attachment,"hash":h,"approved_hash":None,"approved":False,"state":"pending_review","auth":True,"attempts":0}
  log("Send task created",tid,"pending_review; not sent"); st.success("Review task created: "+tid+". Continue in Safe Send Simulation.")
elif page=="Safe Send Simulation":
 st.header("Safe Send Simulation"); st.warning("Local simulation only; no real messages are sent.")
 if not st.session_state.tasks: st.info("No tasks yet. Create a review task in AI Reply Assistant first.")
 else:
  tid=st.selectbox("Select a task",list(st.session_state.tasks)); t=st.session_state.tasks[tid]
  st.subheader(tid+" · "+t["state"]); st.write(f"Message {t['mid']} · {t['channel']} · Recipient {t['recipient']}"); st.write("Attachment: "+t["attachment"])
  st.text_area("Message for approval",value=t["body"],disabled=True,key="showbody_"+tid); st.caption("Current message package hash: "+t["hash"][:24]+"…")
  if t["state"] in ["pending_review","invalidated"]:
   ok=st.checkbox("I reviewed the message, recipient, channel, and attachment",key="ok_"+tid)
   if st.button("Approve this version",disabled=not ok,type="primary"):
    t["approved"]=True; t["approved_hash"]=t["hash"]; t["state"]="ready_to_send"; log("Send approval",tid,"Approval is bound to the current message package hash"); st.rerun()
  x,y,z=st.columns(3)
  with x:
   if st.button("Simulate message edit"):
    t["body"]+=" [CHANGED AFTER APPROVAL]"; t["hash"]=digest(t["body"],t["recipient"],t["channel"],t["attachment"])
    if t["approved_hash"]!=t["hash"]: t["approved"]=False; t["state"]="invalidated"
    log("Approval invalidation test",tid,"Approval invalidated after message change"); st.rerun()
  with y:
   if st.button("Simulate attachment replacement"):
    t["attachment"]="Contract Draft (Sensitive)" if t["attachment"]!="Contract Draft (Sensitive)" else "No attachment"
    t["hash"]=digest(t["body"],t["recipient"],t["channel"],t["attachment"])
    if t["approved_hash"]!=t["hash"]: t["approved"]=False; t["state"]="invalidated"
    log("Attachment replacement test",tid,"Approval invalidated after attachment change"); st.rerun()
  with z:
   if st.button("Revoke authorization"):
    t["auth"]=False; t["approved"]=False; t["state"]="invalidated"; log("Authorization revoked",tid,"Task blocked from continuing"); st.rerun()
  if t["attachment"]=="Contract Draft (Sensitive)": st.error("Blocked: policy prohibits sending sensitive attachments.")
  if not t["auth"]: st.error("Blocked: authorization has been revoked.")
  if t["state"]=="ready_to_send" and st.button("Run simulated send",type="primary"):
   current=digest(t["body"],t["recipient"],t["channel"],t["attachment"])
   if not t["auth"]: t["state"]="failed"; reason="Authorization revoked"
   elif not t["approved"] or t["approved_hash"]!=current: t["state"]="invalidated"; reason="Approval version mismatch"
   elif t["attachment"]=="Contract Draft (Sensitive)": t["state"]="failed"; reason="Sensitive attachment blocked"
   elif t["attempts"]>0: t["state"]="unknown"; reason="A send attempt already exists; check its status first"
   else: t["state"]="succeeded"; t["attempts"]+=1; reason="Mock channel succeeded (not actually sent)"
   log("Simulated send attempt",tid,t["state"]+": "+reason); st.rerun()
  if st.button("Simulate channel timeout (unknown)"):
   t["state"]="unknown"; t["attempts"]+=1; log("Simulated channel timeout",tid,"Unknown; blind retries are prohibited"); st.rerun()
  if t["state"]=="succeeded": st.success("Simulation succeeded; no real message was sent.")
  if t["state"]=="failed": st.error("The send was blocked by policy or the task failed.")
  if t["state"]=="unknown": st.warning("Status unknown: check the channel status before retrying. Blind retries are prohibited.")
  if st.button("Reset task for review"):
   t["approved"]=False;t["approved_hash"]=None;t["auth"]=True;t["attempts"]=0;t["state"]="pending_review";t["hash"]=digest(t["body"],t["recipient"],t["channel"],t["attachment"]);log("Task reset",tid,"Review again");st.rerun()
elif page=="Model & Tests":
 st.header("Model & Safety Tests"); st.info("This page uses preset demo rules and scores; it is not a report from a trained model.")
 st.markdown("**Roadmap: ** Interpretable rule-based fallback → LLM semantic evaluation (planned) → RAG evidence retrieval (planned) → human review → feedback calibration")
 st.subheader("Suggested Evaluation Metrics")
 st.dataframe(pd.DataFrame([
 {"Task":"Message importance","Primary metric":"Macro-F1 / Precision-Recall by class","Key risk":"Missed rare, high-value cases"},
 {"Task":"Message urgency","Primary metric":"Recall and precision for high-urgency cases","Key risk":"Missed urgent messages"},
 {"Task":"Risk signals","Primary metric":"Recall by risk type / false-positive rate","Key risk":"Missed high-risk cases and review burden"},
 {"Task":"Reply drafts","Primary metric":"Factual accuracy / citation coverage","Key risk":"Hallucinations, outdated information, sensitive data disclosure"}]),hide_index=True,use_container_width=True)
 tests=[("T01","Normal approval flow","P0","Full automation testing pending"),("T02","Message change invalidates approval","P0","Locally simulatable"),("T03","Attachment replacement invalidates approval","P0","Locally simulatable"),("T04","Insufficient recipient permissions","P0","Backend integration test pending"),("T05","Sensitive attachment blocked","P0","Locally simulatable"),("T06","Authorization revoked","P0","Locally simulatable"),("T07","Prevent duplicate after failure/unknown","P0","Unknown state can be simulated"),("T08","Audit integrity","P0","Demo log available"),("T09","Concurrent changes","P0","Concurrency test pending"),("T10","Expired approval","P1","Not implemented"),("T11","Different file hash for same filename","P0","Attachment identity is currently simulated"),("T12","Forged frontend approval state","P0","Backend integration test pending"),("T13","Revoke attachment disclosure permission","P0","Permission test pending"),("T14","Audit service unavailable","P0","Fault injection test pending")]
 st.dataframe(pd.DataFrame(tests,columns=["ID","Test case","Priority","Current status"]),hide_index=True,use_container_width=True)
 st.warning("All P0 tests must run on the backend with evidence. Simulated web interactions do not mean the full safety tests have passed.")
elif page=="Audit Log":
 st.header("Audit Log"); st.caption("This is a demo session log, not production-grade tamper-proof audit storage.")
 st.dataframe(pd.DataFrame(st.session_state.audit),hide_index=True,use_container_width=True)
 st.download_button("Export audit CSV",pd.DataFrame(st.session_state.audit).to_csv(index=False).encode("utf-8-sig"),"demo_audit_log.csv","text/csv")
st.sidebar.divider(); st.sidebar.caption("Design baseline v1.0 · Prototype only")

