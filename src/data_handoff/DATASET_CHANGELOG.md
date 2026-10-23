# 版本变更（原版 → large-v2）

- 唯一消息：90 → 9,000（每个平台 30 → 3,000）
- 模拟重复投递：3 → 270
- 虚构联系人：12 → 60（每个联系人的三个平台映射）
- 虚构项目：5 → 15
- 保留最初90条消息，保持归一化字段不变
- 新增 `dataset_config.json`，更新 `validate_output.py` 与 `tests/test_pipeline.py` 的数量检查
- 新增 `synthetic_reference_labels.csv`，供2号做开发验证，不自动喂入正式消息字段
- 维持无网络、无额外 Python 依赖、无需真实平台认证信息
