#!/usr/bin/env python3

import os

script_path = os.path.abspath(__file__)
main_repo_dir = os.path.dirname(os.path.dirname(script_path))
workspace_dir = os.path.dirname(main_repo_dir)


def repo_local_path(repo: str) -> str:
    return os.path.join(workspace_dir, repo)


def read_project_deps(repo_path: str) -> list[str]:
    deps = []
    file_path = os.path.join(repo_path, "project.deps")
    if os.path.exists(file_path):
        with open(file_path) as file:
            for line in file:
                line = line.strip()
                if line != "":
                    deps.append(line)
    return deps


def maven_wrapper() -> str:
    common = os.path.join(workspace_dir, "dbeaver-common", "mvnw")
    if os.name == 'nt':
        common = os.path.join(common, ".cmd")
    return common


def main():
    # Ensure all the needed repos are cloned
    stack = read_project_deps("dbeaver")
    while len(stack) > 0:
        repo = stack.pop()
        repo_path = repo_local_path(repo)
        if not os.path.exists(repo_path):
            os.system(f"git clone https://github.com/dbeaver/{repo}.git -C {repo_path} --depth 1")
            stack.extend(read_project_deps(repo_path))

    profiles = [
        "build-linux-aarch64",
        "build-linux-x86_64",
        "build-macos-aarch64",
        "build-macos-x86_64",
        "build-windows-aarch64",
        "build-windows-x86_64",
        "product-dbeaver-ce",
        "product-dbeaver-eclipse-ce",
        "appstore",
    ]
    profiles_csv = str.join(",", profiles)
    os.system(f"{maven_wrapper()} clean verify -T1C -f {main_repo_dir}{os.sep}product{os.sep}aggregate -P={profiles_csv}")

main()
