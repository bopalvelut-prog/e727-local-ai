# Hardware Compatibility

Community-tested hardware running Primaclaw. Add yours via PR!

## How to add your hardware

```bash
# Run the benchmark
python -m src.efficiency.cli -p "Explain AI in one sentence" --auto --json

# Note the tokens/second and model used
# Add a row to the table below
```

## Tested hardware

| Machine | Year | CPU | RAM | OS | Model | Tokens/s | Contributor |
|---------|------|-----|-----|----|-------|----------|-------------|
| eMachines E727 | 2009 | Intel Pentium T4500 | 4GB | Debian 12 | Qwen2.5 1.5B Q4 | 1.7 | @bopalvelut-prog |
| Acer Swift 3 | 2020 | AMD Ryzen 5 4500U | 8GB | Ubuntu 24.04 | Qwen2.5 3B Q4 | 0.5 | @bopalvelut-prog |
| iPhone 11 (iSH) | 2019 | A13 (x86 emulated) | 4GB | Alpine (iSH) | Qwen2.5 0.5B | ~0.3 | @bopalvelut-prog |
| Raspberry Pi 4 | 2019 | BCM2711 (ARM) | 4GB | Raspberry Pi OS | *not tested* | — | — |
| ThinkPad T420 | 2011 | Intel i5-2520M | 8GB | *not tested* | — | — | — |
| Dell Optiplex 780 | 2009 | Core 2 Duo E8400 | 4GB | *not tested* | — | — | — |

## Minimum requirements

| Resource | Minimum | Recommended |
|----------|---------|-------------|
| CPU | Any x86_64 or ARM | 2+ cores |
| RAM | 1GB | 4GB+ |
| Storage | 2GB | 8GB+ |
| OS | Alpine Linux, Debian, Ubuntu | Any Linux |

## Tips for old hardware

- Use Q4 or Q3 quantization to save memory
- Start with Qwen2.5 0.5B (350MB) — works on almost anything
- Use Alpine Linux for minimal overhead
- Disable swap if using an SSD (wear leveling)
- `renice 19` the worker process for low priority
