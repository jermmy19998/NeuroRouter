# NeuroRouter Demo（中文）

[English README](README.md)

这是一个面向生产演进的“模型路由”演示骨架，完成了你要的完整链路：

1. 用户上传图片
2. 用户说“帮我用 resnet 分类这个图像”
3. 系统解析指令并选择模型别名
4. 调用 Hugging Face 模型推理
5. 返回稳定的结构化 JSON

本仓库定位为 **公开 demo 仓库**。商业核心逻辑建议放在私有仓库，通过适配层接入。

## 1. 能力清单

- 清晰分层：`API / Application / Domain / Infrastructure`
- 可扩展模型注册中心（支持 HF 和后续自定义模型）
- 指令容错解析（`resnet18`、`renet18` 等）
- 统一错误结构
- 单元测试 + API 测试
- GitHub Actions CI
- 发布脚本 `scripts/release.ps1`

## 2. 项目结构

```text
.
├── .github/workflows/ci.yml
├── config/custom-models.example.json
├── scripts/release.ps1
├── src/neurorouter
│   ├── api
│   ├── application
│   ├── core
│   ├── domain
│   ├── infrastructure
│   ├── bootstrap.py
│   └── main.py
├── tests
├── LICENSE
├── README.md
└── README.zh-CN.md
```

## 3. 快速启动

### 3.1 安装依赖

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .[dev]
```

### 3.2 启动服务

```bash
uvicorn neurorouter.main:app --host 0.0.0.0 --port 8000 --reload
```

### 3.3 调用分类接口

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/classify" \
  -F "image=@./examples/cat.jpg" \
  -F "instruction=帮我用resnet分类这个图像" \
  -F "top_k=5"
```

## 4. 返回结构

```json
{
  "request_id": "uuid",
  "input": {
    "instruction": "帮我用resnet分类这个图像",
    "requested_model": null,
    "resolved_model": "resnet18",
    "filename": "cat.jpg",
    "content_type": "image/jpeg"
  },
  "output": {
    "task": "image_classification",
    "predictions": [
      { "label": "tabby, tabby cat", "score": 0.92 }
    ]
  },
  "meta": {
    "engine_source": "huggingface:microsoft/resnet-18",
    "duration_ms": 123,
    "available_models": ["resnet-18", "resnet18"],
    "timestamp": "2026-03-12T12:00:00Z"
  }
}
```

## 5. 扩展更多模型

方案 A：直接在 `src/neurorouter/infrastructure/registry.py` 注册。

方案 B：用外部 JSON 映射文件 + 环境变量：

```bash
set NEUROROUTER_CUSTOM_MODEL_MAP_FILE=config/custom-models.json
```

JSON 格式：

```json
{
  "my-model-alias": "hf:org/model-name"
}
```

## 6. 许可和商业授权

本仓库采用 **source-available demo 许可**（见 `LICENSE`）：

- 允许非商业使用。
- 商业使用必须获得你的书面授权。
- 私有核心模块、私有数据、私有训练流水线不建议放入本公开仓库。

## 7. 发布流程

```powershell
.\scripts\release.ps1 -Version 0.1.0 -Notes "Initial demo release"
```

脚本会自动执行：提交、打 tag、推送、创建 GitHub Release（依赖 `gh` CLI）。
