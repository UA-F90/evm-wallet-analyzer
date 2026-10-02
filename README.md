# EVM Wallet Analyzer

A small Python command-line tool that validates an EVM address and reads its checksum form, chain ID, ETH balance, and transaction count (nonce) from an EVM-compatible JSON-RPC endpoint.

## Requirements

- Python 3.10 or newer
- An EVM JSON-RPC endpoint for the network you want to query

## Install

```bash
python -m venv .venv
```

Activate the environment, then install dependencies:

```powershell
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

```bash
# macOS / Linux
source .venv/bin/activate
```

```bash
python -m pip install -r requirements.txt
```

## Run

Pass an endpoint directly:

```bash
python src/analyzer.py 0x52908400098527886E0F7030069857D2E4169EE7 --rpc "https://YOUR_RPC_ENDPOINT"
```

Or set `RPC_URL` in your shell:

```powershell
$env:RPC_URL = "https://YOUR_RPC_ENDPOINT"
python src/analyzer.py 0x52908400098527886E0F7030069857D2E4169EE7
```

```bash
export RPC_URL="https://YOUR_RPC_ENDPOINT"
python src/analyzer.py 0x52908400098527886E0F7030069857D2E4169EE7
```

The output is JSON. `balance_eth` is a decimal string to preserve precision. The nonce is the number of transactions sent by the address on the selected network. Choose an endpoint for the network you want to inspect; the chain ID identifies the connected network. Keep private or paid RPC URLs out of public commits. `.env.example` is a template and is not loaded automatically.

## Tests

Tests use the standard `unittest` framework and mock Web3, so no internet access or live RPC is needed:

```bash
python -m unittest discover -s tests -v
```

## GitHub Actions

Pushes and pull requests run the unit tests on Python 3.10, 3.11, and 3.12. No RPC secret is needed.

## License

MIT. See [LICENSE](LICENSE).
