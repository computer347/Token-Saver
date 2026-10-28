"""Boilerplate generators for taskbench_app. Usage:
  python3 tools/scaffold.py cli-command NAME   # subparser + dispatch stub in cli.py, plus tests/test_cli_NAME.py
  python3 tools/scaffold.py test-module NAME   # tests/test_NAME.py skeleton
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def cli_command(name: str) -> None:
    cli = ROOT / "taskbench_app" / "cli.py"
    src = cli.read_text()
    var = name.replace("-", "_") + "_cmd"
    parser_anchor = "    return parser\n"
    dispatch_anchor = "    except ValidationError as error:"
    if parser_anchor not in src or dispatch_anchor not in src:
        sys.exit("scaffold: cli.py layout not recognised; add the command by hand")
    src = src.replace(parser_anchor,
                      f'    {var} = commands.add_parser("{name}", help="TODO")\n'
                      f'    # TODO: {var}.add_argument(...)\n' + parser_anchor, 1)
    src = src.replace(dispatch_anchor,
                      f'        elif args.command == "{name}":\n'
                      f'            raise NotImplementedError("TODO: implement {name}")\n' + dispatch_anchor, 1)
    cli.write_text(src)
    test = ROOT / "tests" / f"test_cli_{name.replace('-', '_')}.py"
    if not test.exists():
        test.write_text(
            "from taskbench_app.cli import main\n\n\n"
            f"def test_{name.replace('-', '_')}(tmp_path, capsys):\n"
            "    ledger = str(tmp_path / \"ledger.json\")\n"
            f"    # TODO: arrange, then: assert main([\"--ledger\", ledger, \"{name}\"]) == 0\n"
            "    assert True\n")
    print(f"added '{name}' stubs to taskbench_app/cli.py and created {test.relative_to(ROOT)}")


def test_module(name: str) -> None:
    test = ROOT / "tests" / f"test_{name}.py"
    if test.exists():
        sys.exit(f"{test.relative_to(ROOT)} already exists")
    test.write_text("import pytest\n\n\n"
                    f"def test_{name}_basic():\n    # TODO\n    assert True\n")
    print(f"created {test.relative_to(ROOT)}")


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] not in ("cli-command", "test-module"):
        sys.exit(__doc__)
    (cli_command if sys.argv[1] == "cli-command" else test_module)(sys.argv[2])
