def api_args(parser):
    api_subparser = parser.add_subparsers(dest="api")

    # Create_finetune
    list_model_subparser = api_subparser.add_parser("list_models")
    list_model_subparser.add_argument(
        "--all",
        help="List all models (available and unavailable)",
        default=False,
        action="store_true",
    )
    raw_supply_subparser = api_subparser.add_parser("get_raw_supply")

    return parser