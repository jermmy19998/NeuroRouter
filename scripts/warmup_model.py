from __future__ import annotations

import argparse
from io import BytesIO

from PIL import Image


def warmup(model_id: str) -> None:
    from transformers import pipeline

    image = Image.new("RGB", (32, 32), color=(128, 128, 128))
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    payload = buffer.getvalue()

    classifier = pipeline(task="image-classification", model=model_id)
    classifier(Image.open(BytesIO(payload)).convert("RGB"), top_k=1)


def main() -> None:
    parser = argparse.ArgumentParser(description="Pre-download and warm up an image model.")
    parser.add_argument("--model-id", default="microsoft/resnet-18")
    args = parser.parse_args()

    warmup(args.model_id)
    print(f"Model warmup complete: {args.model_id}")


if __name__ == "__main__":
    main()

