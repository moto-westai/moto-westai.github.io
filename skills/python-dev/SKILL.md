---
name: python-dev
description: Python development with OOP/MVC patterns, FastAPI, and production best practices. Use when the user asks to write, review, debug, refactor, or architect Python code. Covers class design, project structure, async patterns, testing, documentation, and code quality.
---

# Python Development

## Standards

- Python 3.10+ (3.12 preferred)
- OOP with clean class hierarchies
- MVC pattern for application architecture
- Well-documented source code (docstrings on all public classes/methods)
- Type hints everywhere

## Project Structure (MVC)

```
project/
├── app/
│   ├── __init__.py
│   ├── main.py              # Entry point
│   ├── config.py             # Settings (pydantic-settings)
│   ├── models/               # Data models (SQLAlchemy, Pydantic)
│   │   ├── __init__.py
│   │   └── user.py
│   ├── views/                # API routes / endpoints
│   │   ├── __init__.py
│   │   └── user_routes.py
│   ├── controllers/          # Business logic
│   │   ├── __init__.py
│   │   └── user_controller.py
│   ├── services/             # External integrations
│   │   └── __init__.py
│   └── utils/                # Helpers
│       └── __init__.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_user.py
├── requirements.txt
├── pyproject.toml
├── Dockerfile
└── README.md
```

## Code Style

### Classes & Docstrings

```python
class InferenceClient:
    """Client for communicating with local LLM inference endpoints.

    Handles connection pooling, retries, and streaming responses
    for OpenAI-compatible APIs.

    Attributes:
        base_url: The inference server base URL.
        timeout: Request timeout in seconds.
    """

    def __init__(self, base_url: str, timeout: float = 30.0) -> None:
        self.base_url = base_url
        self.timeout = timeout
        self._client: httpx.AsyncClient | None = None

    async def generate(self, prompt: str, **kwargs) -> str:
        """Generate a completion from the inference server.

        Args:
            prompt: The input prompt text.
            **kwargs: Additional generation parameters.

        Returns:
            The generated text response.

        Raises:
            ConnectionError: If the server is unreachable.
        """
        ...
```

### FastAPI Patterns

```python
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter(prefix="/api/v1", tags=["inference"])

@router.post("/generate", response_model=GenerateResponse)
async def generate(
    request: GenerateRequest,
    controller: InferenceController = Depends(get_controller),
) -> GenerateResponse:
    """Generate text from the inference engine."""
    try:
        result = await controller.generate(request)
        return GenerateResponse(text=result)
    except ServiceUnavailable as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e),
        )
```

### Async Best Practices

- Use `httpx.AsyncClient` over `requests` for async code
- Use `asyncio.gather()` for concurrent operations
- Always use `async with` for client lifecycle
- Avoid blocking calls in async contexts

## Testing

```bash
# Run tests
pytest -v

# With coverage
pytest --cov=app --cov-report=term-missing
```

Use pytest with fixtures. Test public interfaces, not internals.

## Documentation Requirements

- Module-level docstrings explaining purpose
- Class docstrings with attributes
- Method docstrings with Args/Returns/Raises (Google style)
- Type hints on all function signatures
- Inline comments only for non-obvious logic

## Guidelines

- Prefer composition over inheritance
- Use Pydantic for data validation and settings
- Use `pathlib.Path` over `os.path`
- Use f-strings over `.format()` or `%`
- Handle errors explicitly — no bare `except:`
- Use `logging` module, not `print()` for production code
- Before writing code, confirm requirements and approach with user
- For large changes, propose the architecture first
