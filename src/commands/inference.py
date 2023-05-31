def inference_args(parser):
    parser.add_argument("--model", default=None, help="name/path of the model")
    parser.add_argument(
        "--max-tokens",
        default=128,
        type=int,
        help="the maximum number of tokens to generate",
    )
    parser.add_argument(
        "--sample",
        default=True,
        action="store_true",
        help="indicates whether to sample",
    )
    parser.add_argument(
        "--temperature", default=0.6, type=float, help="temperature for the LM"
    )
    parser.add_argument("--top-k", default=40, type=int, help="top-k for the LM")

    parser.add_argument(
        "--all",
        default=False,
        action="store_true",
        help="list all models (available and unavailable)",
    )

    return parser
