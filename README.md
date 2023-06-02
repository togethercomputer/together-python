Python client for Together's Cloud Platform

## What can it do?
The Together Python client can:
- Access the Together API
  - List available/all models
- Run inference
- Upload training/validation files/datasets to the Together Cloud
- Make finetune requests  

## Installation
### From Source
1. `pip install git+https://github.com/togethercomputer/together.git`
2. Run `together --help` to see available commands

## Contributing
1. Clone the repo and make your changes
2. Run `pip install together['quality']`
3. From the root of the repo, run
    - `black .`
    - `ruff .`
      - And if necessary, `ruff . --fix`
    - `mypy --strict .`
4. Create a PR
