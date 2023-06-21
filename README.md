Python client for Together's Cloud Platform

## Installation
`pip install git+https://github.com/togethercomputer/together.git`

OR
1. Clone this repo
2. `pip install -e .`

Run `together --help` to see available commands

## Contributing
1. Clone the repo and make your changes
2. Run `pip install together['quality']`
3. From the root of the repo, run
    - `black .`
    - `ruff .`
      - And if necessary, `ruff . --fix`
    - `mypy --strict .`
4. Create a PR
