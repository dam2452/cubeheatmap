# Contributing to cubeheatmap

Thanks for your interest! Contributions are welcome.

## How to contribute

1. **Fork** the repository
2. Create a **feature branch** (`git checkout -b feature/my-feature`)
3. Make your changes
4. Run the tests: `pytest tests/ -v`
5. Run the examples: `cd examples && python generate_all.py`
6. Open a **Pull Request** with a clear description

## Development setup

```bash
git clone https://github.com/dam2452/cubeheatmap.git
cd cubeheatmap
pip install -e ".[dev]"
```

## Running tests

```bash
pytest tests/ -v
```

## Code style

- Python 3.10+
- Follow existing code style (type hints, dataclasses, `from __future__ import annotations`)
- Keep the public API stable - new features should extend, not break
- Add examples for new features
- Add tests for new functionality

## Adding a new preset

1. Create a new module in `cubeheatmap/presets/`
2. Import it in `cubeheatmap/presets/__init__.py`
3. Add an example in `examples/`
4. Functions should return `(CubeHeatmap, Style)` tuples from `to_heatmap()`

## Reporting issues

Open a [GitHub Issue](https://github.com/dam2452/cubeheatmap/issues) with:
- Python version and OS
- Minimal reproducible example
- Expected vs actual behavior
