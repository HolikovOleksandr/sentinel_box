import subprocess as p
from result_model import CommandResult


def run_command(command):
    try:
        result = p.run(
            command, 
            capture_output=True, 
            text=True
        )

        return CommandResult(
            ok=result.returncode == 0,
            returncode=result.returncode,
            stdout=result.stdout,
            stderr=result.stderr,
        )

    except FileNotFoundError as err:
        return CommandResult(
            ok=False,
            returncode=None,
            stdout="",
            stderr=str(err),
        )

print(run_command(["pwd"]))