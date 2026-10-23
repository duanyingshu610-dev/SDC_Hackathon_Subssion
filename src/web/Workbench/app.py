import streamlit as st
import pandas as pd, hashlib, uuid
from datetime import datetime
st.set_page_config(page_title="Orbyte | AI 客户工作台",page_icon="✦",layout="wide")
if "messages" not in st.session_state:
 st.session_state.messages=[
 {"id":"MSG-2401","time":"20:54","channel":"WhatsApp","account":"Northstar Trading","sender":"Mia Chen","body":"The shipment for PO-8842 still hasn't arrived. Our warehouse closes at 18:00 tomorrow. Can you confirm the delivery status tonight?","importance":92,"urgency":96,"risk":"交付时限","reason":"明确要求今晚确认，且涉及明日仓库关闭和订单交付。","status":"待处理"},
 {"id":"MSG-2402","time":"20:31","channel":"Email","account":"BluePeak Retail","sender":"Daniel Wong","body":"Could you send the latest product catalogue and the updated wholesale price list for Q4?","importance":71,"urgency":48,"risk":"资料外发检查","reason":"涉及产品目录与价格表，需核对版本和披露权限。","status":"待处理"},
 {"id":"MSG-2403","time":"19:48","channel":"Discord","account":"Cedar Labs","sender":"Evan Li","body":"We noticed an unexpected change in the billing destination. Please pause the transfer until we verify this with your finance team.","importance":97,"urgency":93,"risk":"付款/欺诈风险","reason":"付款目的地异常变更，客户要求暂停并核验。","status":"风险复核"},
 {"id":"MSG-2404","time":"18:20","channel":"WhatsApp","account":"BluePeak Retail","sender":"Daniel Wong","body":"Thanks for the quick turnaround last week. The samples look good.","importance":39,"urgency":18,"risk":"无明显风险信号","reason":"一般性反馈，没有明确时限或高影响事项。","status":"已查看"},
 {"id":"MSG-2405","time":"17:56","channel":"Email","account":"Northstar Trading","sender":"Mia Chen","body":"Please confirm whether the revised invoice includes the agreed shipping credit of USD 1,250.","importance":84,"urgency":72,"risk":"发票/金额核对","reason":"涉及具体金额与发票条款，需核对已批准记录。","status":"待处理"},
 {"id":"MSG-2406","time":"16:43","channel":"WhatsApp","account":"Harborline Supply","sender":"Sofia Tan","body":"No rush—just checking if the onboarding guide is available when you have a chance.","importance":28,"urgency":12,"risk":"无明显风险信号","reason":"客户明确表示不急，是一般资料请求。","status":"待处理"}]
if "accounts" not in st.session_state:
 st.session_state.accounts={
 "Northstar Trading":{"industry":"批发贸易","stage":"稳定交易","value":88,"growth":72,"risk":"低","attention":"重点关注","facts":"历史订单稳定；当前有交付时限和发票核对事项。"},
 "BluePeak Retail":{"industry":"零售渠道","stage":"成长合作","value":71,"growth":84,"risk":"低","attention":"普通关注","facts":"近期索取 Q4 产品目录和批发价目表。"},
 "Cedar Labs":{"industry":"科技 / 实验室","stage":"合作中","value":64,"growth":69,"risk":"待复核","attention":"普通关注","facts":"出现付款目的地异常变更信号。账户价值不能降低风险处理优先级。"},
 "Harborline Supply":{"industry":"供应链","stage":"初步合作","value":43,"growth":51,"risk":"未知","attention":"低频关注","facts":"当前消息为低紧急度资料询问。"}}
if "audit" not in st.session_state: st.session_state.audit=[{"时间":"启动","事件":"加载演示数据","对象":"系统","结果":"仅本地模拟"}]
if "tasks" not in st.session_state: st.session_state.tasks={}
if "drafts" not in st.session_state: st.session_state.drafts={}
def log(event,obj,result):
 st.session_state.audit.insert(0,{"时间":datetime.now().strftime("%H:%M:%S"),"事件":event,"对象":obj,"结果":result})
def digest(body,recipient,channel,attachment):
 return hashlib.sha256("|".join([body,recipient,channel,attachment]).encode()).hexdigest()
def box(label,value,sub):
 st.markdown(f'<div style="border:1px solid #e5eaf1;border-radius:14px;padding:16px;background:white"><div style="color:#667085;font-size:12px">{label}</div><div style="font-size:27px;font-weight:700;color:#172554">{value}</div><div style="color:#667085;font-size:11px">{sub}</div></div>',unsafe_allow_html=True)
st.markdown("""<style>.block-container{padding-top:1.2rem;max-width:1500px}.hero{padding:24px 28px;border-radius:18px;color:white;background:linear-gradient(120deg,#172554,#4058a6);margin-bottom:18px}.hero h1{color:white;margin:0}.hero p{color:#dbe5ff;margin:5px 0 0}.muted{color:#667085;font-size:12px}</style>""",unsafe_allow_html=True)
st.sidebar.markdown("# ✦ ORBYTE")
st.sidebar.caption("AI 商业客户消息工作台")
page=st.sidebar.radio("工作区",["总览仪表盘","消息工作台","客户账户","AI 回复助手","安全发送模拟","模型与测试","审计日志"])
st.sidebar.divider(); st.sidebar.success("本地演示模式")
st.sidebar.caption("无真实渠道连接 · 无外部 AI API · 不会真实发送")
M=st.session_state.messages; A=st.session_state.accounts
if page=="总览仪表盘":
 st.markdown('<div class="hero"><h1>客户消息，清晰判断，安全行动。</h1><p>多渠道聚合 · AI 优先级评估 · 个人关注 · 人工审核回复</p></div>',unsafe_allow_html=True)
 c=st.columns(4)
 for col,l,v,s in zip(c,["演示消息","高紧急消息","待处理事项","客户账户"],[len(M),sum(m["urgency"]>=80 for m in M),sum(m["status"] in ["待处理","风险复核"] for m in M),len(A)],["3 个模拟渠道","紧急度 ≥ 80","含风险复核","个人关注设置独立"]):
  with col: box(l,v,s)
 st.write(""); left,right=st.columns([1.3,1])
 with left:
  st.subheader("优先处理队列")
  for m in sorted(M,key=lambda x:(x["urgency"]>=80,x["importance"]),reverse=True)[:5]:
   with st.container(border=True):
    st.markdown(f"**{'🔴' if m['urgency']>=85 else '🟠' if m['urgency']>=60 else '🟢'} {m['account']} · {m['sender']}**")
    st.caption(f"{m['channel']} · {m['time']} · {m['risk']}")
    st.write(m["body"]); st.write(f"重要性 **{m['importance']}** / 100　|　紧急度 **{m['urgency']}** / 100")
 with right:
  st.subheader("客户账户与风险")
  st.dataframe(pd.DataFrame([{"客户":k,"关注级别":v["attention"],"账户评估":v["value"],"付款风险":v["risk"]} for k,v in A.items()]),hide_index=True,use_container_width=True)
  st.info("账户长期价值不会覆盖当前消息的紧急程度或风险告警。")
elif page=="消息工作台":
 st.header("消息工作台"); st.caption("演示分数仅用于验证界面与工作流，不是正式模型预测。")
 c=st.columns(3)
 with c[0]: channel=st.selectbox("渠道",["全部","WhatsApp","Email","Discord"])
 with c[1]: urgency=st.selectbox("紧急度",["全部","高 ≥80","中 50–79","低 <50"])
 with c[2]: query=st.text_input("搜索客户或消息")
 filtered=[m for m in M if (channel=="全部" or m["channel"]==channel) and (urgency=="全部" or (urgency=="高 ≥80" and m["urgency"]>=80) or (urgency=="中 50–79" and 50<=m["urgency"]<80) or (urgency=="低 <50" and m["urgency"]<50)) and (not query or query.lower() in (m["account"]+m["body"]+m["sender"]).lower())]
 left,right=st.columns([1,1.3])
 with left:
  for m in sorted(filtered,key=lambda x:x["urgency"],reverse=True):
   with st.container(border=True):
    st.markdown(f"**{m['account']}** · {m['channel']} · {m['time']}")
    st.write(m["body"][:140])
    st.caption(f"重要性 {m['importance']} · 紧急度 {m['urgency']} · {m['status']}")
    if st.button("查看详情",key="view_"+m["id"]): st.session_state.selected=m["id"]
 with right:
  ids=[m["id"] for m in filtered]
  if not ids: st.info("没有符合条件的消息。")
  else:
   default=st.session_state.get("selected",ids[0]); m=next((x for x in filtered if x["id"]==default),filtered[0])
   st.subheader(m["account"]+" · "+m["sender"]); st.caption(m["id"]+" · "+m["channel"])
   st.markdown(f"> {m['body']}")
   x,y=st.columns(2)
   with x: st.metric("AI 重要性（模拟）",str(m["importance"])+"/100")
   with y: st.metric("AI 紧急度（模拟）",str(m["urgency"])+"/100")
   st.warning("风险提示："+m["risk"]); st.write("**判断依据：** "+m["reason"])
   st.write("**建议：** 先核实业务事实；高风险事项进入人工复核。模型分数不能授权发送或付款。")
   if st.button("标记已查看",key="mark_"+m["id"]): m["status"]="已查看"; log("消息状态更新",m["id"],"已查看"); st.rerun()
elif page=="客户账户":
 st.header("客户账户"); st.caption("个人关注级别是工作偏好，不是 AI 对客户价值的判断。")
 name=st.selectbox("选择客户",list(A)); a=A[name]
 c=st.columns(4)
 for col,l,v,s in zip(c,["账户评估（模拟）","成长潜力（模拟）","付款风险","个人关注"],[f"{a['value']}/100",f"{a['growth']}/100",a["risk"],a["attention"]],[a["industry"],a["stage"],"需要证据核验","仅当前演示用户"]):
  with col: box(l,v,s)
 left,right=st.columns(2)
 with left:
  st.subheader("账户概况"); st.write("**行业：**",a["industry"]); st.write("**关系阶段：**",a["stage"]); st.write(a["facts"])
  rel=[m for m in M if m["account"]==name]
  st.subheader("关联消息"); st.dataframe(pd.DataFrame([{"时间":m["time"],"渠道":m["channel"],"重要性":m["importance"],"紧急度":m["urgency"],"风险":m["risk"]} for m in rel]),hide_index=True,use_container_width=True)
 with right:
  st.subheader("个人关注设置")
  level=st.radio("关注级别",["重点关注","普通关注","低频关注"],index=["重点关注","普通关注","低频关注"].index(a["attention"]),key="lvl_"+name)
  sound=st.selectbox("声音",["跟随等级","明显提示音","普通提示音","轻提示/静音"],key="snd_"+name)
  visual=st.selectbox("视觉标记",["自动","星标","蓝点","无额外标记"],key="vis_"+name)
  quiet=st.checkbox("遵守静音时段 22:00–08:00",value=True,key="q_"+name)
  if st.button("保存个人设置",type="primary"):
   old=a["attention"]; a["attention"]=level; log("个人关注设置变更",name,f"{old} → {level}; 声音={sound}; 视觉={visual}; 静音={quiet}")
   st.success("已保存到当前演示会话；不修改 AI 评估，也不与团队共享。")
  st.info("长期账户评估变化只提醒用户，不自动修改手动关注等级。")
elif page=="AI 回复助手":
 st.header("AI 回复与资料助手"); st.caption("当前使用本地演示模板，不调用外部 AI API。")
 mid=st.selectbox("选择消息",[m["id"] for m in M]); m=next(x for x in M if x["id"]==mid)
 st.write(f"客户：**{m['account']}** · 渠道：{m['channel']}"); st.markdown("> "+m["body"])
 knowledge={
 "Northstar Trading":"订单状态须从订单系统确认；发票折让需对照已批准条款。演示环境没有真实订单系统数据。",
 "BluePeak Retail":"产品目录与 Q4 批发价目表对外发送前，需核对版本和披露权限。",
 "Cedar Labs":"付款目的地异常变更需暂停相关动作，并通过已验证的内部财务联系人核验。",
 "Harborline Supply":"可提供入门指南；发送前确认版本和对外披露许可。"}
 st.info("检索到的模拟资料："+knowledge[m["account"]])
 defaults={
 "MSG-2401":"Hi Mia, thanks for flagging this. I’m checking the latest status for PO-8842 with our operations team. I’ll confirm the verified delivery status and next steps as soon as I have an update.",
 "MSG-2402":"Hi Daniel, happy to help. I’ll verify the latest approved Q4 catalogue and wholesale price list, including document versions and sharing permissions, before sending them over.",
 "MSG-2403":"Hi Evan, thank you for alerting us. We will pause any action related to the changed billing destination while finance verifies the request through an established contact channel.",
 "MSG-2404":"Hi Daniel, glad to hear the samples look good. Thanks for the feedback — we’ll be happy to help with next steps when you’re ready.",
 "MSG-2405":"Hi Mia, I’ll compare the revised invoice against the approved shipping-credit terms and confirm the amount once it has been verified.",
 "MSG-2406":"Hi Sofia, I’ll confirm the latest onboarding guide version and share it once I’ve verified that it is approved for external distribution."}
 if mid not in st.session_state.drafts: st.session_state.drafts[mid]=defaults[mid]
 body=st.text_area("回复草稿（可编辑）",value=st.session_state.drafts[mid],height=150,key="draft_"+mid); st.session_state.drafts[mid]=body
 recipient=st.text_input("收件人",value=m["sender"],key="to_"+mid)
 attachment=st.selectbox("附件候选",["无附件","Q4 产品目录 v3.2","批发价目表 v2026-Q4","订单状态摘要（内部）","合同草案（敏感）"],key="att_"+mid)
 if attachment=="合同草案（敏感）": st.error("敏感附件：模拟策略将阻止直接发送。")
 st.write("发送前：人工检查正文、收件人、渠道、附件版本和对外披露权限。")
 if st.button("保存草稿"):
  log("回复草稿保存",mid,"仅保存本地草稿；未发送"); st.success("已保存草稿。")
 if st.button("创建待审核任务",type="primary",disabled=not recipient.strip()):
  tid="SEND-"+uuid.uuid4().hex[:8].upper(); h=digest(body,recipient,m["channel"],attachment)
  st.session_state.tasks[tid]={"id":tid,"mid":mid,"body":body,"recipient":recipient,"channel":m["channel"],"attachment":attachment,"hash":h,"approved_hash":None,"approved":False,"state":"pending_review","auth":True,"attempts":0}
  log("创建发送任务",tid,"pending_review；未发送"); st.success("已创建待审核任务："+tid+"。前往「安全发送模拟」继续。")
elif page=="安全发送模拟":
 st.header("安全发送模拟"); st.warning("只运行本地模拟流程；不会发送真实消息。")
 if not st.session_state.tasks: st.info("暂无任务。请先在 AI 回复助手创建待审核任务。")
 else:
  tid=st.selectbox("选择任务",list(st.session_state.tasks)); t=st.session_state.tasks[tid]
  st.subheader(tid+" · "+t["state"]); st.write(f"消息 {t['mid']} · {t['channel']} · 收件人 {t['recipient']}"); st.write("附件："+t["attachment"])
  st.text_area("审批正文",value=t["body"],disabled=True,key="showbody_"+tid); st.caption("当前发送包哈希："+t["hash"][:24]+"…")
  if t["state"] in ["pending_review","invalidated"]:
   ok=st.checkbox("我已检查正文、收件人、渠道和附件",key="ok_"+tid)
   if st.button("批准当前版本",disabled=not ok,type="primary"):
    t["approved"]=True; t["approved_hash"]=t["hash"]; t["state"]="ready_to_send"; log("发送审批",tid,"审批绑定当前发送包哈希"); st.rerun()
  x,y,z=st.columns(3)
  with x:
   if st.button("模拟正文被修改"):
    t["body"]+=" [CHANGED AFTER APPROVAL]"; t["hash"]=digest(t["body"],t["recipient"],t["channel"],t["attachment"])
    if t["approved_hash"]!=t["hash"]: t["approved"]=False; t["state"]="invalidated"
    log("审批失效测试",tid,"正文变更后审批失效"); st.rerun()
  with y:
   if st.button("模拟替换附件"):
    t["attachment"]="合同草案（敏感）" if t["attachment"]!="合同草案（敏感）" else "无附件"
    t["hash"]=digest(t["body"],t["recipient"],t["channel"],t["attachment"])
    if t["approved_hash"]!=t["hash"]: t["approved"]=False; t["state"]="invalidated"
    log("附件替换测试",tid,"附件变化后审批失效"); st.rerun()
  with z:
   if st.button("撤销授权"):
    t["auth"]=False; t["approved"]=False; t["state"]="invalidated"; log("授权撤销",tid,"阻止任务继续"); st.rerun()
  if t["attachment"]=="合同草案（敏感）": st.error("阻断：敏感附件策略禁止直接发送。")
  if not t["auth"]: st.error("阻断：授权已撤销。")
  if t["state"]=="ready_to_send" and st.button("执行模拟发送",type="primary"):
   current=digest(t["body"],t["recipient"],t["channel"],t["attachment"])
   if not t["auth"]: t["state"]="failed"; reason="授权已撤销"
   elif not t["approved"] or t["approved_hash"]!=current: t["state"]="invalidated"; reason="审批版本不匹配"
   elif t["attachment"]=="合同草案（敏感）": t["state"]="failed"; reason="敏感附件阻断"
   elif t["attempts"]>0: t["state"]="unknown"; reason="已有发送尝试，需先查状态"
   else: t["state"]="succeeded"; t["attempts"]+=1; reason="Mock channel 模拟成功（非真实发送）"
   log("模拟发送尝试",tid,t["state"]+": "+reason); st.rerun()
  if st.button("模拟渠道超时（unknown）"):
   t["state"]="unknown"; t["attempts"]+=1; log("模拟渠道超时",tid,"unknown；禁止盲目重试"); st.rerun()
  if t["state"]=="succeeded": st.success("模拟成功；没有任何真实消息发出。")
  if t["state"]=="failed": st.error("发送被策略阻止或任务失败。")
  if t["state"]=="unknown": st.warning("状态未知：先查询渠道状态，禁止盲目重发。")
  if st.button("重置任务为待审核"):
   t["approved"]=False;t["approved_hash"]=None;t["auth"]=True;t["attempts"]=0;t["state"]="pending_review";t["hash"]=digest(t["body"],t["recipient"],t["channel"],t["attachment"]);log("任务重置",tid,"重新审核");st.rerun()
elif page=="模型与测试":
 st.header("模型与安全测试"); st.info("当前为预置演示规则和分数，不是正式训练模型报告。")
 st.markdown("**目标路线：** 可解释规则兜底 → LLM 语义评估（未来接入）→ RAG 证据检索（未来接入）→ 人工复核 → 反馈校准")
 st.subheader("评估指标建议")
 st.dataframe(pd.DataFrame([
 {"任务":"消息重要性","主指标":"Macro-F1 / 每类 Precision-Recall","重点风险":"低频高价值类别漏报"},
 {"任务":"消息紧急度","主指标":"高紧急类别 Recall + Precision","重点风险":"紧急消息漏报"},
 {"任务":"风险信号","主指标":"分类型 Recall / 误报率","重点风险":"高风险漏报与复核负担"},
 {"任务":"回复草稿","主指标":"事实正确率 / 引用覆盖率","重点风险":"幻觉、过期资料、敏感信息外发"}]),hide_index=True,use_container_width=True)
 tests=[("T01","正常审批路径","P0","待完整自动化测试"),("T02","正文变更使审批失效","P0","可本地模拟"),("T03","附件替换使审批失效","P0","可本地模拟"),("T04","收件人权限不足","P0","待后端集成测试"),("T05","敏感附件阻断","P0","可本地模拟"),("T06","授权撤销","P0","可本地模拟"),("T07","失败/unknown 防重复","P0","可模拟 unknown"),("T08","审计完整性","P0","演示日志可查看"),("T09","并发修改","P0","待并发测试"),("T10","审批过期","P1","待实现"),("T11","同名不同文件哈希","P0","当前仅模拟附件标识"),("T12","伪造前端审批状态","P0","待后端集成测试"),("T13","撤销附件披露权","P0","待权限测试"),("T14","审计服务不可用","P0","待故障注入测试")]
 st.dataframe(pd.DataFrame(tests,columns=["ID","用例","级别","当前状态"]),hide_index=True,use_container_width=True)
 st.warning("所有 P0 测试必须在后端真实执行并留证。网页内交互模拟不代表完整安全测试通过。")
elif page=="审计日志":
 st.header("审计日志"); st.caption("当前为演示会话日志，非生产级不可篡改审计存储。")
 st.dataframe(pd.DataFrame(st.session_state.audit),hide_index=True,use_container_width=True)
 st.download_button("导出审计 CSV",pd.DataFrame(st.session_state.audit).to_csv(index=False).encode("utf-8-sig"),"demo_audit_log.csv","text/csv")
st.sidebar.divider(); st.sidebar.caption("设计基线 v1.0 · Prototype only")
