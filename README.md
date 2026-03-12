# NeuroRouter Demo

[中文说明](README.zh-CN.md)

NeuroRouter Demo is a production-oriented skeleton for model routing:

- Upload an image
- Send an instruction like: `help me use resnet to classify this image`
- Resolve target model alias
- Run inference via Hugging Face
- Return a stable structured JSON response

This repository is intentionally a **demo-only public codebase**. Keep your commercial/core logic in a private repository and integrate through adapters.

## 1. Features

- Layered architecture (API / Application / Domain / Infrastructure)
- Model registry for future growth (Hugging Face and custom aliases)
- Typo-tolerant instruction parsing (`resnet18`, `renet18`, etc.)
- Unified error schema
- Unit/API tests
- GitHub Actions CI workflow
- Release helper script (`scripts/release.ps1`)

## 2. Project Structure

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

## 3. Quick Start

### 3.1 Install

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .[dev]
```

### 3.2 Run API

```bash
uvicorn neurorouter.main:app --host 0.0.0.0 --port 8000 --reload
```

### 3.3 Call Inference

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/classify" \
  -F "image=@./examples/cat.jpg" \
  -F "instruction=help me use resnet to classify this image" \
  -F "top_k=5"
```

## 4. Response Schema

```json
{
  "request_id": "uuid",
  "input": {
    "instruction": "help me use resnet to classify this image",
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

## 5. Add More Models

Option A: Register in code (`src/neurorouter/infrastructure/registry.py`).

Option B: Provide a JSON model map and set env var:

```bash
set NEUROROUTER_CUSTOM_MODEL_MAP_FILE=config/custom-models.json
```

JSON format:

```json
{
  "my-model-alias": "hf:org/model-name"
}
```

## 6. License and Commercial Use

This repository uses a **source-available demo license** (see `LICENSE`):

- Non-commercial use is allowed.
- Commercial use requires your explicit written authorization.
- Keep proprietary modules/models/private datasets outside this public repo.

## 7. Release Workflow

```powershell
.\scripts\release.ps1 -Version 0.1.0 -Notes "Initial demo release"
```

This script commits, tags, pushes, and creates a GitHub release via `gh`.
