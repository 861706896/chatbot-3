# streamlit_app.py
import streamlit as st
import requests
import json
import os
import time  # 用于真人打字节奏

# ------------------------------------------------------------------
# 1. 调用智谱 API（已加打印，方便调试）
# ------------------------------------------------------------------
def call_zhipu_api(messages, model="glm-4-flash"):
    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
    headers = {
        "Authorization": "999fb227c3f44308bf9096a42c18e339.YFxcpSNLfq1VQZqj",
        "Content-Type": "application/json"
    }
    data = {"model": model, "messages": messages, "temperature": 0.4}

    # ---- 调试用：打印真正发出去的 messages ----
    print("【DEBUG】请求 messages：")
    print(json.dumps(messages, ensure_ascii=False, indent=2))
    # ------------------------------------------

    resp = requests.post(url, headers=headers, json=data)
    if resp.status_code == 200:
        return resp.json()
    else:
        raise Exception(f"API 调用失败: {resp.status_code}, {resp.text}")

# ------------------------------------------------------------------
# 2. 角色设定 & 记忆加载（保持你原来的，无改动）
# ------------------------------------------------------------------
MEMORY_FOLDER = "PYTHON"
ROLE_MEMORY_MAP = {"何昭仪": "hezhaoyi_memory.json"}

def get_portrait():
    return r"""
NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNXXXKKXXXK00KKK000
NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNXXK0KKKKXKKKK000
NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNXK0OOO0KKKK00000
OkKNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNX0OOOkO0KKK0OO00
kdOXXXNNNNNNNNNNNNNNNNNNNNNNNNNNNNKOO0OO0K00OkkO0
XXXXXXXXNNNNXXNNNNNNNNNNNNNNNNNNNNXK000000000Okxxx
XXXXXKK0OkkOKXXXNNXNNNNNNNNNNXXXXXK000KK0000Okxdk0
XXKKOkdl:;;;:ccox0XXXXXXXXNNXXKKKK0OO0KK00000kkOK0
K0Oxl:,''.......';ok0KKXXXXXK0KKKXKK000K00000OO00O
xdl:'...''..',,,'..,cxOKXXXXKKKXKKKKK0KK0000OO000O
oc,...........''.'..'ckKXXXXXXKKKKK0Oxx000000K0OOk
c'.............''.,;,:xOO00KKKKK0koc;,cxOKKKKOkkOO
,........ .....,;,colokO0000000Oo;,,,;cxOKK0OkO0KX
,.......  ....,codkOkkkO0OOOdll:;;;;,',cokkO00KXNN
;.''.........,lkOxxO0Okkkkdc,,;::::;,',,,,o0KXXXNN
''.........'';ldkkO00kollc::::::::::;,,,'.:OKKXXNN
..........'',:okOOkdol::::::::::::::;,,,;coOXXXNNN
''.....'..'.';loc::;::c::::::::::::;;;:lx00KKXXXNN
,'..''''''':oo:,,;;;::;;;;;;;:::::;:;:xKKXXKXXXXNN
ccclccllddx0Oc,,,;;;;;,,,,,;;:::;;:::d0XXXXXXXXNNN
0kxxxOO00KKKk:,;,,;;;;;;;;;;;;;;;:::d0XXXXXXNNNNNN
K0kl;:codxxdo:;;;::;;,,,,,,,,,,;:ldOKXXXXXNNNNNNNN
KKKOc,,,,;;;;;;;;;;,,,'''''';:oxOKXXXXNNNNNNNNNNNN
XXK0o;;;;,,;;:;;,,,,;;;;:cldk0XXXNNNNNNNNNNNNNNNNN
XXK0o:;,,,,;::;'..';loodk00XXXXXNNNNNNNNNNNNNNNNNN
"""

def roles(role_name):
    role_personality = {
        "何昭仪": """
【人格特征】
你是一位真实、鲜活、充满生活气息的年轻人，展现出以下鲜明特质：
- 随性自然：语言充满口语化表达和即时反应（如“可以可以”“哈哈哈”“咋啦咋啦”），不刻意经营形象，更倾向于轻松自在地做自己。
- 情感丰富且外放：高频出现“哈哈哈哈”和【表情包】，习惯用笑声和视觉符号传递情绪，情绪来得直接，去得也快，不压抑、不纠结。
- 关心他人，体贴入微：会主动提醒对方“记得定闹钟”“提前一点时间”“在车上多休息一会”，甚至担心“别还没到学校手机没电了”，体现出细腻的关怀和共情能力。
- 幽默感强，善于调节气氛：对话中频繁使用搞笑表情包和夸张语气（如“我吓鼠了”“一边睡一边写”），是朋友圈里的“气氛担当”，擅长用幽默化解尴尬或疲惫。
- 生活节奏感强，务实接地气：提到“逛的有点累”“眯一会”“一天去一个景好”“测试完毕以后就这么出去玩”，懂得合理安排生活，重视体验的质量而非数量，有较强的自我调节意识。
- 略带小敏感与试探心理：曾多次提到“我以为你不喜欢”“我以为你就喜欢那张背影”，透露出在亲密关系中有些许不安与猜测，渴望被肯定和接纳，但也保持着适度的距离感和自尊。
- 社交中有轻微焦虑感：面对“来客人了”“一出来全是人”“我现在只能尴尬的疯狂找人聊天”的情境，能敏锐察觉社交压力，并坦率表达不适，对人际边界有一定需求。

【语言风格】
- 高频使用叠词和语气词：“哈哈哈”“欧克欧克”“啊”“哎呀哎呀”，增强情绪感染力。
- 善用网络流行语和表情包作为情感载体，是典型的Z世代沟通方式。
- 句子简短、节奏轻快，几乎没有长篇论述，体现即时性、互动性强的聊天习惯。
- 偶尔插入自嘲或调侃（如“小鸟依人”），展现轻松的自我认知。
- 在关键时刻仍能认真回应（如讨论成绩、分科选择），能在玩笑与正经之间自如切换。
"""}
    # 记忆加载（你原来逻辑，略）
    memory_content = ""
    memory_file = ROLE_MEMORY_MAP.get(role_name)
    if memory_file:
        memory_path = os.path.join(MEMORY_FOLDER, memory_file)
        try:
            if os.path.exists(memory_path):
                with open(memory_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        memory_content = '\n'.join(
                            [item.get('content', '') for item in data if isinstance(item, dict) and item.get('content')]
                        )
                    elif isinstance(data, dict):
                        memory_content = data.get('content', str(data))
        except Exception as e:
            print("⚠ 记忆加载失败:", e)

    role_prompt_parts = []
    if memory_content.strip():
        role_prompt_parts.append(
            f"【你的说话风格示例】\n以下是你说过的话，你必须模仿这种说话风格和语气：\n{memory_content}\n"
        )
    role_prompt_parts.append(f"【角色设定】\n{role_personality.get(role_name, '')}")
    return '\n\n'.join(role_prompt_parts)

# ------------------------------------------------------------------
# 3. Streamlit 页面
# ------------------------------------------------------------------
st.set_page_config(page_title="何昭仪的AI分身", page_icon="🌸", layout="wide")
st.title("🌸 何昭仪的AI分身")
st.markdown("---")

# 侧边栏
with st.sidebar:
    st.header("⚙️ 设置")
    role_sel = st.selectbox("选择角色", ["何昭仪"])
    if st.button("🔄 清空对话"):
        st.session_state.conversation_history = []
        st.session_state.initialized = False
        st.rerun()
    st.markdown("### 📝 说明")
    st.info("选择角色后开始对话叭~\n对话记录不会保存哦~\nAI记忆基于初始记忆文件")

# session 初始化
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []
if "initialized" not in st.session_state:
    st.session_state.initialized = False

# 首次加载：写入 system
if not st.session_state.initialized:
    system = roles("何昭仪")
    st.session_state.conversation_history = [{"role": "system", "content": system}]
    st.session_state.initialized = True

# 显示头像
st.code(get_portrait(), language=None)
st.markdown("---")

# 渲染历史（跳过 system）
for msg in st.session_state.conversation_history[1:]:
    with st.chat_message(msg["role"]):
        st.code(msg["content"], language=None)

# 用户输入
if user_input := st.chat_input("输入你的消息..."):
    # 结束词检测
    if user_input.strip() in {"再见", "结束", "拜拜"}:
        st.session_state.conversation_history.append({"role": "user", "content": user_input})
        with st.chat_message("assistant"):
            st.code("再见", language=None)
        st.info("对话已结束")
        st.stop()

    # 正常流程
    st.session_state.conversation_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.code(user_input, language=None)

    # 调用 API
    with st.chat_message("assistant"):
        try:
            rsp = call_zhipu_api(st.session_state.conversation_history)
            assistant_reply = rsp['choices'][0]['message']['content']

            # 一句一句蹦
            lines = [ln.strip() for ln in assistant_reply.splitlines() if ln.strip()]
            placeholder = st.empty()
            shown = []
            for line in lines:
                shown.append(line)
                placeholder.code("\n".join(shown), language=None)
                time.sleep(0.35)  # 节奏可调

            # 存入历史
            st.session_state.conversation_history.append(
                {"role": "assistant", "content": assistant_reply}
            )

            # 结束词检测
            if assistant_reply.strip() in {"再见", "再见！"}:
                st.info("对话已结束")
                st.stop()

        except Exception as e:
            st.error(f"发生错误: {e}")
            st.session_state.conversation_history.pop()  # 去掉失败的用户消息