import os
import subprocess
import sys
from argparse import ArgumentParser
from logging import getLogger
from pathlib import Path

from dotenv import load_dotenv

logger = getLogger(__name__)


def check_gq_exists() -> bool:
    try:
        proc = subprocess.run(
            args=["gq", "--version"],
            stdout=subprocess.DEVNULL,
        )

        return proc.returncode == 0
    except OSError:
        # Command not exists
        return False


def fetch_hasura_graphql_schema(
    hasura_graphql_endpoint: str,
    hasura_graphql_token: str,
) -> str:
    proc = subprocess.run(
        args=[
            "gq",
            "--introspect",
            hasura_graphql_endpoint,
            "--header",
            f"Authorization: Bearer {hasura_graphql_token}",
        ],
        capture_output=True,
    )

    return proc.stdout.decode(encoding="utf-8")


def main() -> None:
    load_dotenv()

    env_hasura_graphql_endpoint: str | None = (
        os.environ.get("AMATERUS_CRAWLER_HASURA_GRAPHQL_ENDPOINT") or None
    )
    env_hasura_graphql_token = (
        os.environ.get("AMATERUS_CRAWLER_HASURA_GRAPHQL_TOKEN") or None
    )

    parser = ArgumentParser()
    parser.add_argument(
        "--hasura_graphql_endpoint",
        type=str,
        default=env_hasura_graphql_endpoint,
        required=env_hasura_graphql_endpoint is None,
    )
    parser.add_argument(
        "--hasura_graphql_token",
        type=str,
        default=env_hasura_graphql_token,
        required=env_hasura_graphql_token is None,
    )
    parser.add_argument(
        "-o",
        "--output_file",
        type=Path,
        default="schema.graphql",
    )
    args = parser.parse_args()

    hasura_graphql_endpoint: str = args.hasura_graphql_endpoint
    hasura_graphql_token: str = args.hasura_graphql_token
    output_file: Path = args.output_file

    gq_exist = check_gq_exists()
    if not gq_exist:
        logger.error("gq (hasura/graphqurl) is not installed: npm install -g graphqurl")
        sys.exit(1)

    hasura_graphql_schema_text = fetch_hasura_graphql_schema(
        hasura_graphql_endpoint=hasura_graphql_endpoint,
        hasura_graphql_token=hasura_graphql_token,
    )
    output_file.write_text(
        hasura_graphql_schema_text,
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
