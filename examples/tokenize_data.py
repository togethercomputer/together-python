import argparse
import logging
from functools import partial
from multiprocessing import cpu_count
from typing import Dict, List

from datasets import Dataset, load_dataset  # type: ignore
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


def tokenize_variable_length(
    data: Dict[str, str],
    tokenizer: PreTrainedTokenizerBase,
    add_special_tokens: bool = True,
) -> BatchEncoding:
    tokenized = tokenizer(data["text"], add_special_tokens=add_special_tokens, truncation=False)
    return tokenized


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


def pack_sequences(
    batch: BatchEncoding,
    max_seq_len: int,
    pad_token_id: int,
    eos_token_id: int,
    add_labels: bool,
    cutoff_size: int = 0,
) -> Dict[str, List[List[int]]]:
    """
    cutoff_size = max_seq_len means that we will drop any non-full sequences
        (full packing without padding)
    Example:
        Sequence 1:
        ['<s>', '▁usually', '▁,', '▁he', '▁would', '▁be', '▁t', 'earing']
        Sequence 2:
        ['▁around', '▁the', '▁living', '▁room', '▁,', '▁playing', '▁with', '▁his']
        Sequence 3:
        ['▁toys', '▁.', '</s>', '<s>', '▁but', '▁just', '▁one', '▁look']
    """
    packed_sequences = []
    buffer = []

    for input_ids in batch["input_ids"]:
        # Add the current sequence to the buffer
        buffer.extend(input_ids)
        buffer.append(eos_token_id)  # Add EOS at the end of each sequence

        # Check if buffer needs to be split into chunks
        while len(buffer) > max_seq_len:
            # Take a full chunk from the buffer and append it to packed_sequences
            packed_sequences.append(buffer[:max_seq_len])
            # Remove the processed chunk from the buffer
            buffer = buffer[max_seq_len:]

    # Add the last buffer if it's exactly chunk_size
    if len(buffer) == max_seq_len:
        packed_sequences.append(buffer)
    elif len(buffer) > cutoff_size:
        # if the buffer is larger than the cutoff size, pad it to the chunk_size
        # if not, we do not include in the packed_sequences
        buffer.extend([pad_token_id] * (max_seq_len - len(buffer)))
        packed_sequences.append(buffer)

    output = {"input_ids": packed_sequences}
    if add_labels:
        output["labels"] = [
            [LOSS_IGNORE_INDEX if token_id == pad_token_id else token_id for token_id in example]
            for example in output["input_ids"]
        ]

    # mask attention for padding tokens, a better version would also mask cross-sequence dependencies
    output["attention_mask"] = [
        [0 if token_id == pad_token_id else 1 for token_id in example]
        for example in output["input_ids"]
    ]
    return output


def process_fast_packing(
    dataset: Dataset,
    tokenizer: PreTrainedTokenizerBase,
    max_sequence_length: int,
    add_labels: bool,
    add_special_tokens: bool,
) -> Dataset:
    tokenized_dataset = dataset.map(
        lambda examples: tokenize_variable_length(
            examples, tokenizer, add_special_tokens=add_special_tokens
        ),
        batched=True,
        num_proc=cpu_count(),
        load_from_cache_file=True,
        remove_columns=dataset.column_names,
    )
    logger.info(f"tokenized dataset: {tokenized_dataset}")

    packed_dataset = tokenized_dataset.map(
        lambda batch: pack_sequences(
            batch,
            max_sequence_length,
            tokenizer.pad_token_id,
            tokenizer.eos_token_id,
            add_labels=add_labels,
            cutoff_size=max_sequence_length,
        ),
        batched=True,
        num_proc=cpu_count() if len(tokenized_dataset) > 10000 else 1,
        remove_columns=["attention_mask"],
    )
    logger.info(f"Packed dataset: {packed_dataset}")
    return packed_dataset


def process_data(args: argparse.Namespace) -> None:
    if not args.out_filename.endswith(".parquet"):
        raise ValueError("`--out_filename` should have the `.parquet` extension")

    dataset = load_dataset(args.dataset, split="train")
    tokenizer = AutoTokenizer.from_pretrained(args.tokenizer)
    tokenizer.pad_token = tokenizer.eos_token

    dataset.to_json("dataset.jsonl", orient="records", lines=True)

    if not args.packing:
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
    else:
        tokenized_data = process_fast_packing(
            dataset,
            tokenizer,
            max_sequence_length=args.max_seq_length,
            add_labels=args.add_labels,
            add_special_tokens=True,
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
    print(len(tokenized_data[0]["input_ids"]))
    tokenized_data.to_parquet(args.out_filename)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pretokenize examples for finetuning via Together")
    parser.add_argument(
        "--dataset",
        type=str,
        default="clam004/antihallucination_dataset",
        help="Dataset name on the Hugging Face Hub",
    )
    parser.add_argument("--max-seq-length", type=int, default=8192, help="Maximum sequence length")
    parser.add_argument(
        "--add-labels",
        action="store_true",
        help="Whether to add loss labels from padding tokens",
    )
    parser.add_argument(
        "--tokenizer",
        type=str,
        required=True,
        help="Tokenizer name (for example, togethercomputer/Llama-3-8b-hf)",
    )
    parser.add_argument(
        "--out-filename",
        default="processed_dataset.parquet",
        help="Name of the Parquet file to save (should have .parquet extension)",
    )
    parser.add_argument(
        "--packing",
        action="store_true",
        help="Whether to pack shorter sequences up to `--max-seq-length`",
    )
    args = parser.parse_args()

    process_data(args)
