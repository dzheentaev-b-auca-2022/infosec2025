from cli import parse_args, dispatch


def main() -> None:
    args = parse_args()
    dispatch(args)


if __name__ == "__main__":
    main()
