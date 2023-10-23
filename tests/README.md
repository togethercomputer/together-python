# How to run tests
>  🚧 Warning: test_finetune.py can take a while. Please have at least one prior successful finetuning run in your account for successful results. 

>  🚧 Please have enough space on disk to download your lastest successful fine-tuned model's weights into the `tests` directory of this repo. All downloaded files will be deleted after successful test runs but may not be deleted if tests fail.

1. Clone the repo locally
```bash
git clone https://github.com/togethercomputer/together.git
```
2. Change directory
```bash
cd together
```
3. [Optional] Checkout the commit you'd like to test
```bash
git checkout COMMIT_HASH
```
4. Install together package and dependencies
```bash
pip install . && pip install .['tests']
```
5. Change directory into `tests`
```bash
cd tests
```
6. Export API key
```bash
export TOGETHER_API_KEY=<API_KEY>
```
7. Run pytest
```bash
pytest
```