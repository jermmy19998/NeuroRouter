from neurorouter.application.instruction_parser import InstructionModelResolver


def test_resolve_from_explicit_model() -> None:
    resolver = InstructionModelResolver()
    assert (
        resolver.resolve(
            instruction="帮我用resnet分类这个图像",
            explicit_model="custom-model",
            default_model="resnet18",
        )
        == "custom-model"
    )


def test_resolve_from_instruction_typo() -> None:
    resolver = InstructionModelResolver()
    assert (
        resolver.resolve(
            instruction="please use renet18 to classify this image",
            explicit_model=None,
            default_model="resnet18",
        )
        == "resnet18"
    )


def test_resolve_default_when_instruction_empty() -> None:
    resolver = InstructionModelResolver()
    assert resolver.resolve(instruction=None, explicit_model=None, default_model="resnet18") == "resnet18"

