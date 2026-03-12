from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from neurorouter.api.routes import router as inference_router
from neurorouter.api.schemas import ErrorResponse
from neurorouter.core.config import get_settings
from neurorouter.domain.errors import (
    InferenceEngineError,
    InvalidInputError,
    ModelNotFoundError,
    NeuroRouterError,
)

settings = get_settings()
app = FastAPI(title=settings.app_name, version=settings.app_version)
app.include_router(inference_router)


def _error_response(status_code: int, code: str, message: str) -> JSONResponse:
    payload = ErrorResponse(error_code=code, message=message).model_dump()
    return JSONResponse(status_code=status_code, content=payload)


@app.exception_handler(ModelNotFoundError)
async def model_not_found_handler(_: Request, exc: ModelNotFoundError) -> JSONResponse:
    return _error_response(404, "MODEL_NOT_FOUND", str(exc))


@app.exception_handler(InvalidInputError)
async def invalid_input_handler(_: Request, exc: InvalidInputError) -> JSONResponse:
    return _error_response(400, "INVALID_INPUT", str(exc))


@app.exception_handler(InferenceEngineError)
async def inference_engine_handler(_: Request, exc: InferenceEngineError) -> JSONResponse:
    return _error_response(500, "INFERENCE_ENGINE_ERROR", str(exc))


@app.exception_handler(NeuroRouterError)
async def generic_neurorouter_handler(_: Request, exc: NeuroRouterError) -> JSONResponse:
    return _error_response(400, "NEUROROUTER_ERROR", str(exc))

