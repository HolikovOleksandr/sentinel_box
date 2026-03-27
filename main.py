from shell_utils import run_command

pwd_result = run_command(["pwd"])

if pwd_result.ok:
    print(pwd_result.stdout)
else:
    print(pwd_result.stderr)