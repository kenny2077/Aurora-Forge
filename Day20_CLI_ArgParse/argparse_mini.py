"""A tiny hand-rolled argument parser for our CLI.

Supports:
    --verbose                 boolean flag
    --output <file>           or  --output=<file>
    --retries <n>             or  --retries=<n>   (integer; default 3)
    positional args           anything not starting with '--'
    --                        end-of-options marker: everything after is positional

Bug reports:
  - `--output=out.txt` (the '=' form) is treated as a positional instead of setting output.
  - `--retries 5` stores the string "5", not the int 5.
  - An unknown option like `--nope` is silently swallowed as a positional instead of erroring.
  - `--` isn't handled, so `-- --verbose` wrongly sets verbose.

Fix parse() to satisfy test_argparse_mini.py.

Contract: parse(argv) -> dict with keys: verbose(bool), output(str|None), retries(int),
positional(list[str]). Unknown '--option' raises ValueError.
"""


def parse(argv):
    result = {"verbose": False, "output": None, "retries": 3, "positional": []}
    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg == "--verbose":
            result["verbose"] = True
        elif arg == "--output":
            i += 1
            result["output"] = argv[i]
        elif arg == "--retries":
            i += 1
            result["retries"] = argv[i]
        else:
            result["positional"].append(arg)
        i += 1
    return result
