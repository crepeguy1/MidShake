# midshake_lsp.py
#
# A minimal Language Server Protocol implementation
# using only Python's built-in libraries.
#
# Works with Python 3.14 and requires NO external packages.

import sys
import json
import threading
from midshake_interpreter import check_errors


# ------------------------------------------------------------
# Helper: read a single LSP message from stdin
# ------------------------------------------------------------
def read_message():
    headers = {}
    while True:
        line = sys.stdin.readline()
        if not line:
            return None
        line = line.strip()
        if line == "":
            break
        key, value = line.split(":", 1)
        headers[key.strip()] = value.strip()

    length = int(headers.get("Content-Length", 0))
    if length == 0:
        return None

    body = sys.stdin.read(length)
    return json.loads(body)


# ------------------------------------------------------------
# Helper: send a JSON-RPC message to the client
# ------------------------------------------------------------
def send_message(payload):
    body = json.dumps(payload)
    sys.stdout.write(f"Content-Length: {len(body)}\r\n\r\n{body}")
    sys.stdout.flush()


# ------------------------------------------------------------
# Publish diagnostics to VS Code
# ------------------------------------------------------------
def publish_diagnostics(uri, text):
    errors = check_errors(text)
    diagnostics = []

    for err in errors:
        diagnostics.append({
            "range": {
                "start": {"line": err["line"], "character": 0},
                "end": {"line": err["line"], "character": len(err["message"])}
            },
            "severity": 1,  # Error
            "source": "midshake",
            "message": err["message"]
        })

    send_message({
        "jsonrpc": "2.0",
        "method": "textDocument/publishDiagnostics",
        "params": {
            "uri": uri,
            "diagnostics": diagnostics
        }
    })


# ------------------------------------------------------------
# Main LSP loop
# ------------------------------------------------------------
def run_server():
    open_docs = {}

    while True:
        msg = read_message()
        if msg is None:
            break

        method = msg.get("method")

        # Client opened a document
        if method == "textDocument/didOpen":
            uri = msg["params"]["textDocument"]["uri"]
            text = msg["params"]["textDocument"]["text"]
            open_docs[uri] = text
            publish_diagnostics(uri, text)

        # Client changed a document
        elif method == "textDocument/didChange":
            uri = msg["params"]["textDocument"]["uri"]
            text = msg["params"]["contentChanges"][0]["text"]
            open_docs[uri] = text
            publish_diagnostics(uri, text)

        # Initialize request
        elif method == "initialize":
            send_message({
                "jsonrpc": "2.0",
                "id": msg.get("id"),
                "result": {
                    "capabilities": {
                        "textDocumentSync": 1  # full sync
                    }
                }
            })

        # Shutdown request
        elif method == "shutdown":
            send_message({"jsonrpc": "2.0", "id": msg.get("id"), "result": None})
            return

        # Exit notification
        elif method == "exit":
            return


if __name__ == "__main__":
    run_server()
