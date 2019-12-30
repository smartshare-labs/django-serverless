import os
import json
import subprocess


def parse_param(param_input):
    split_param = param_input.split("=")

    if len(split_param) == 1:
        return split_param[0], None
    else:
        return split_param[0], "".join(split_param[1:])


def set_ssm_param(key, value, profile="default"):
    output = subprocess.check_output(
        f"aws ssm put-parameter  --name {key} --value {value} --type String --profile {profile} --overwrite",
        shell=True,
    )
    version = json.loads(output)
    print(version)


def get_ssm_param(key, profile="default"):
    output = subprocess.check_output(
        f"aws ssm get-parameter  --name {key} --profile {profile}", shell=True,
    )
    parameter = json.loads(output).get("Parameter")
    if parameter:
        return parameter["Value"]


def list_ssm_params(profile="default"):
    output = subprocess.check_output(
        f"aws ssm describe-parameters --profile {profile}", shell=True
    )
    params = json.loads(output)

    print("\nExisting parameters: \n")
    for p in params.get("Parameters", []):
        print(f"\t{p['Name']}")


def run():
    aws_profile = os.getenv("AWS_PROFILE")
    list_ssm_params(profile=aws_profile)

    print("\n###############################################\n")
    param_input = input("Get/Set Param (e.g. ABC=DEF to set, ABC to get): ")
    key, value = parse_param(param_input)

    if value:
        set_ssm_param(key, value, profile=aws_profile)
    else:
        value = get_ssm_param(key, profile=aws_profile)
        print(f"'{value}'")


if __name__ == "__main__":
    run()
