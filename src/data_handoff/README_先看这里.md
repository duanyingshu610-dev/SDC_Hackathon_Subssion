# SDC Domain 2 — 1号成员大样本模拟接入包（v2）

**从90条扩充到9,000条唯一合成消息（每个平台3,000条）。**
另外含270条模拟重复投递事件，供去重测试。最初90条消息全部保留。

## 在 PyCharm 中运行
1. `File → Open`，打开整个 `SDC_Domain2_Member1_Integration_Kit_Large` 文件夹。
2. 右键 `run_demo.py` → Run。
3. 右键 `validate_output.py` → Run，期待看到 `PASS`。
4. 也可打开 Terminal，运行 `python -m unittest discover -s tests -v`。
5. 生成的交接文件位于 `output/`，详见 `integration_guide.md`。

预计结果：Raw events = 9,270；Normalized messages = 9,000；Duplicates removed = 270；Failed events = 0。

**重要：本包只演示模拟消息读取、归一化、去重和身份映射。它不会连接或发送真实 WhatsApp / Email / Discord 消息。**

`data/reference/synthetic_reference_labels.csv` 是**场景设计时指定的参考标签**，不是人工标注的真实样本，也不能直接当作 AI 模型在真实工作消息上的可靠准确率证明。
