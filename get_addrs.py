import requests
import json
from os import getenv
from pathlib import Path
import subprocess
import sys

rpc_user = getenv("RPC_USER")
rpc_password = getenv("RPC_PASSWORD")
rpc_url = getenv("RPC_URL")
rpc_port = getenv("RPC_PORT") or 8332
bitcoin_dir = getenv("BITCOIN_DIR")

addrs_file = "addrs.json"

def query_rpc():
    headers = {
        'content-type': 'application/json'
    }

    payload = json.dumps({
        'jsonrpc': '1.0',
        'id': 'curltest',
        'method': 'getnodeaddresses',
        'params': [0]
    })

    response = requests.post(f"{rpc_url}:{rpc_port}", headers=headers, data=payload, auth=(rpc_user, rpc_password))
    return response


def main():
    """Main entry point for the script"""
    import argparse

    parser = argparse.ArgumentParser(description="Query getnodeaddresses and optionally run ASmap diff on them.")
    parser.add_argument("--old-file", default=None,
                        help="Older ASmap file")
    parser.add_argument("--new-file", default=None,
                        help="Newer ASmap file")
    parser.add_argument("--output-dir", default=".",
                        help="Directory to store diff files")

    args = parser.parse_args()

    response = query_rpc()
    if response.status_code == 200:
        addrs_data = response.json()["result"]
        with open(addrs_file, 'w') as f:
            f.write(json.dumps(addrs_data, indent=4))
            print(f"Wrote addrs file: {addrs_file}")
    else:
        print(f"Error: {response.status_code}")
        sys.exit()

    if args.old_file and args.new_file:
        cmd = [
            "python3", Path(bitcoin_dir) / "contrib/asmap/asmap-tool.py",
            "diff_addrs",
            str(args.old_file),
            str(args.new_file),
            addrs_file
              ]

        result = subprocess.run(cmd, capture_output=True, check=False)

        if result.stdout:
            output_file = str(Path(args.output_dir) / 'output.txt')
            with open(output_file, 'w') as f:
                f.write(result.stdout.decode())
                print(f"Wrote diff file: {output_file}!")
        else:
            print("Diff failed.")

if __name__ == "__main__":
    sys.exit(main())
