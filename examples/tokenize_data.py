import argparse
import logging
from functools import partial
from multiprocessing import cpu_count
from typing import Dict

from datasets import load_dataset  # type: ignore
from transformers import (  # type: ignore
    AutoTokenizer,
    BatchEncoding,
    PreTrainedTokenizerBase,
)


# see default of ignore_index
# for https://pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html#torch.nn.CrossEntropyLoss
LOSS_IGNORE_INDEX = -100

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def tokenize_constant_length(
    data: Dict[str, str],
    tokenizer: PreTrainedTokenizerBase,
    max_length: int = 2048,
    add_special_tokens: bool = True,
    add_labels: bool = True,
) -> BatchEncoding:
    # tokenized contains `input_ids` and `attention_mask`
    tokenized: BatchEncoding = tokenizer(
        data["text"],
        max_length=max_length,
        truncation=True,
        padding="max_length",
        add_special_tokens=add_special_tokens,
    )
    # add labels to mask out any padding tokens
    if add_labels:
        tokenized["labels"] = [
            LOSS_IGNORE_INDEX if token_id == tokenizer.pad_token_id else token_id
            for token_id in tokenized["input_ids"]
        ]

    return tokenized


def process_data(args: argparse.Namespace) -> None:
    if not args.out_filename.endswith(".parquet"):
        raise ValueError("`--out_filename` should have the `.parquet` extension")

    dataset = load_dataset(args.dataset, split="train")
    tokenizer = AutoTokenizer.from_pretrained(args.tokenizer)
    tokenizer.pad_token = tokenizer.eos_token

    tokenized_data = dataset.map(
        partial(
            tokenize_constant_length,
            tokenizer=tokenizer,
            max_length=args.max_seq_length,
            add_special_tokens=True,
            add_labels=args.add_labels,
        ),
        batched=False,
        num_proc=cpu_count(),
        remove_columns=dataset.column_names,
    )

    assert (
        "input_ids" in tokenized_data.column_names
        and "attention_mask" in tokenized_data.column_names
    )

    if args.add_labels:
        assert "labels" in tokenized_data.column_names

    logger.info("Tokenized data:")
    print(tokenized_data)

    logger.info(f"Saving data to {args.out_filename}")
    tokenized_data.to_parquet(args.out_filename)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Pretokenize examples for finetuning via Together"
    )
    parser.add_argument(
        "--dataset",
        type=str,
        default="clam004/antihallucination_dataset",
        help="Dataset name on the Hugging Face Hub",
    )
    parser.add_argument(
        "--max-seq-length", type=int, default=2048, help="Maximum sequence length"
    )
    parser.add_argument(
        "--add_labels",
        action="store_true",
        help="Whether to add loss labels from padding tokens",
    )
    parser.add_argument(
        "--tokenizer",
        type=str,
        default="togethercomputer/LLaMA-2-7B-32K",
        help="Tokenizer name (for example, togethercomputer/LLaMA-2-7B-32K)",
    )
    parser.add_argument(
        "--out_filename",
        default="processed_dataset.parquet",
        help="Name of the Parquet file to save (should have .parquet extension)",
    )
    args = parser.parse_args()

    process_data(args)
