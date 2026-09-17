"""service_config loader for the API gateway.

Our gateway reads an INI-style `service.conf` on boot and binds a socket to `[server] port`.
Last night staging fell over: the gateway couldn't read `[server] port` as an int at all, so
`socket.bind` blew up on startup. Between mangled keys, un-stripped values, and ignored inline
comments, the config comes back wrong in several ways. The parser below is what loads that config —
and its test suite (test_config.py) is now failing. Read it, understand it, fix it.

Public API:
    parse_config(text: str) -> dict[str, dict]      # section -> {key: coerced value}
    load_server_settings(text) -> dict              # convenience accessor used at boot
"""


def _coerce(value):
    """Turn a raw string value into a bool / int / float / str."""
    if value.isdigit():
        return int(value)
    if value == "true":
        return True
    if value == "false":
        return bool(value)
    return value


def parse_config(text):
    """Parse INI-style config text into a dict of sections."""
    sections = {}
    current = "DEFAULT"
    sections[current] = {}

    for line in text.split("\n"):
        # skip blank lines and comments
        if line == "":
            continue
        if line[0] == "#":
            continue

        # section header, e.g. [server]
        if line[0] == "[" and line[-1] == "]":
            current = line[1:-1]
            sections[current] = {}
            continue

        # key = value
        if "=" not in line:
            continue
        key, value = line.split("=")

        section = sections[current]
        if key not in section:
            section[key] = _coerce(value)

    return sections


def load_server_settings(text):
    """What the gateway actually calls at boot. If coercion is wrong, `port` is a str here
    and the caller's `socket.bind(("", port))` raises TypeError — that's the staging outage."""
    cfg = parse_config(text)
    return cfg.get("server", {})


if __name__ == "__main__":
    # Quick manual repro of the outage.
    # Healthy output: keys have no trailing spaces and `port` is the int 9090.
    sample = "[server]\nhost = localhost\nport = 9090   # prod port\ndebug = true\n"
    settings = load_server_settings(sample)
    print("parsed server settings:", settings)
    print("keys:", list(settings.keys()), "(should be ['host', 'port', 'debug'])")
    print("port value:", repr(settings.get("port")), "(should be 9090)")
    print("port type:", type(settings.get("port")).__name__, "(should be 'int')")
