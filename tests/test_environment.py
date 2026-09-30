from inf8239_u01.environment import environment_message

def test_environment_message():
    assert environment_message() == "Entorno INF-8239 listo"

def environment_message() -> str:
    return "Entorno INF-8239 listo"

import sys, platform

print(sys.executable)
print(sys.version)
print(platform.platform())

assert ".venv" in sys.executable.lower()