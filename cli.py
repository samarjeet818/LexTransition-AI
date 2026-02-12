from __future__ import annotations

import argparse
import json
import sys

from engine.mapping_logic import map_ipc_to_bns
from engine.rag_engine import index_pdfs, search_pdfs
from engine.db import (
    import_mappings_from_csv,
    import_mappings_from_excel,
    backup_database,
    restore_database,
)
from engine.config import get_runtime_diagnostics


def _cmd_map(args: argparse.Namespace) -> int:
    result = map_ipc_to_bns(args.ipc_section)
    if not result:
        print("No mapping found")
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def _cmd_import(args: argparse.Namespace) -> int:
    if args.file.lower().endswith(".csv"):
        success_count, errors = import_mappings_from_csv(args.file)
    elif args.file.lower().endswith(".xlsx"):
        success_count, errors = import_mappings_from_excel(args.file)
    else:
        print("Only .csv or .xlsx files are supported")
        return 2
    print(json.dumps({"success_count": success_count, "errors": errors}, ensure_ascii=False, indent=2))
    return 0 if success_count > 0 and not errors else (1 if success_count > 0 else 2)


def _cmd_search(args: argparse.Namespace) -> int:
    index_pdfs(args.dir)
    result = search_pdfs(args.query, top_k=args.top_k)
    if not result:
        print("No grounded citation found")
        return 1
    print(result)
    return 0


def _cmd_backup(args: argparse.Namespace) -> int:
    backup_path = backup_database(args.path)
    if not backup_path:
        print("Backup failed")
        return 1
    print(backup_path)
    return 0


def _cmd_restore(args: argparse.Namespace) -> int:
    ok = restore_database(args.path)
    if not ok:
        print("Restore failed")
        return 1
    print("Restore successful")
    return 0


def _cmd_diagnostics(_: argparse.Namespace) -> int:
    print(json.dumps(get_runtime_diagnostics(), ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="LexTransition-AI CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    map_cmd = sub.add_parser("map", help="Map IPC section to BNS")
    map_cmd.add_argument("ipc_section")
    map_cmd.set_defaults(func=_cmd_map)

    import_cmd = sub.add_parser("import", help="Import mappings from CSV/Excel")
    import_cmd.add_argument("--file", required=True)
    import_cmd.set_defaults(func=_cmd_import)

    search_cmd = sub.add_parser("search", help="Search grounded citations in PDFs")
    search_cmd.add_argument("--query", required=True)
    search_cmd.add_argument("--dir", default="law_pdfs")
    search_cmd.add_argument("--top-k", type=int, default=3)
    search_cmd.set_defaults(func=_cmd_search)

    backup_cmd = sub.add_parser("backup-db", help="Backup mapping DB")
    backup_cmd.add_argument("--path", default=None)
    backup_cmd.set_defaults(func=_cmd_backup)

    restore_cmd = sub.add_parser("restore-db", help="Restore mapping DB")
    restore_cmd.add_argument("--path", required=True)
    restore_cmd.set_defaults(func=_cmd_restore)

    diag_cmd = sub.add_parser("diagnostics", help="Show runtime diagnostics")
    diag_cmd.set_defaults(func=_cmd_diagnostics)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    sys.exit(main())
