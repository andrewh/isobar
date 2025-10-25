# Contributing

## Code style

To run a style check with flake8:

```
flake8 isobar
```

### Import style

Avoid wildcard imports (`from isobar import *`). Always import only the symbols you use. This improves readability, clarifies provenance, and helps static analysis. Example:

```
from isobar import Pattern, Timeline, Note
```

If you need many related pattern classes, prefer importing the module and qualifying, rather than a large explicit list:

```
from isobar import pattern
scale = pattern.Scale([...])
```

Do not introduce wildcard imports in new examples, tests, or library code.

## Testing

To run unit tests:

```
python3 setup.py test
```

To generate a unit test coverage report:

```
pip3 install pytest-cov
pytest --cov=isobar tests
```

To automatically run unit tests on commit:
```
echo pytest > .git/hooks/pre-commit
```

### Clock timing expectations

Timing tests use `time.perf_counter()` for higher resolution. The internal clock aims for low jitter but typical macOS / CPython scheduling can occasionally exceed 2 ms. Current test tolerance allows upper jitter ≤ 4 ms while asserting that average intervals remain close to target. When proposing precision improvements:

- Provide reproducible measurements (script or test) using `perf_counter()`.
- Avoid OS-specific real-time APIs unless strictly required by a demonstrated musical use case.
- Keep changes minimal and focused; justify any increase in complexity with clear data.

Sub‑2 ms guarantees are deferred until a concrete requirement emerges; discuss first before implementing platform-specific paths.

## Documentation

To generate and serve the docs:

```
pip3 install mkdocs mkdocs-material
mkdocs serve
```

To deploy docs to GitHub:
```
mkdocs gh-deploy
```

To regenerate the per-class pattern docs for the pattern library docs and README:

```
auxiliary/scripts/generate-docs.py -m > docs/patterns/library.md
auxiliary/scripts/generate-docs.py
```

## Distribution

To push to PyPi:

* increment version in `setup.py`
* `git tag vx.y.z`, `git push --tags`, and create GitHub release
* `python3 setup.py sdist`
* `twine upload dist/isobar-x.y.z.tar.gz`
