"""
Utility functions for HaslettCLI.
"""
import os
import sys
import click
import yaml

def load_profile_data(profile_name, profiles_dir):
    """
    Loads profile data from a YAML file.
    """
    profile_path = os.path.join(profiles_dir, profile_name)
    if not os.path.exists(profile_path):
        click.echo(f"Error: Profile ''{profile_name}'' not found in ''{profiles_dir}'.")
        sys.exit(1)

    with open(profile_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data
