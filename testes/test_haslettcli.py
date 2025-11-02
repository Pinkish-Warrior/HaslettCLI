# tests/test_haslettcli.py
import os
import subprocess

def test_init():
    subprocess.run(["python", "haslettcli.py", "init", "test_project"])
    assert os.path.isdir("test_project/templates")
    assert os.path.isdir("test_project/profiles")

def test_add_profile():
    subprocess.run(["python", "haslettcli.py", "add-profile", "dummy_profile.yml"])
    assert os.path.exists("profiles/dummy_profile.yml")