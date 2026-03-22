# Contributing to Primaclaw

Thanks for wanting to help! Here's how to get started.

## What we need help with

### Good first issues
- Add more model metadata (origin, license) to the efficiency module
- Test on Raspberry Pi 4/5 and report results
- Improve the dashboard UI
- Add TLS support for the coordinator

### Bigger projects
- Support for llama.cpp workers (not just Ollama)
- Automatic model selection based on hardware benchmarks
- WebRTC-based P2P communication between workers
- Kubernetes/Helm chart for cloud deployment

## How to contribute

1. Fork the repo
2. Create a feature branch: `git checkout -b my-feature`
3. Make your changes
4. Run linting: `ruff check src/`
5. Test your changes locally
6. Submit a PR with a clear description

## Adding your hardware

The best contribution right now is testing on your old hardware. Run the benchmark:

```bash
python -m src.efficiency.cli -p "Hello" --auto --json -o my_hardware.json
```

Open a PR adding your results to [HARDWARE.md](HARDWARE.md).

## Code style

- Python 3.9+ compatible
- Use type hints where possible
- Keep functions small and testable
- No heavy dependencies (we target old hardware)

## Community

- [GitHub Discussions](https://github.com/bopalvelut-prog/e727-local-ai/discussions)
- [HARDWARE.md](HARDWARE.md) — community-tested hardware list

## License

By contributing, you agree your code will be MIT licensed.
