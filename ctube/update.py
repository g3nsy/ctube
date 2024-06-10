import requests


def get_latest_version(pkg_name: str) -> str:
    res = requests.get(f"https://pypi.org/pypi/{pkg_name}/json")
    return res.json()["info"]["version"]
