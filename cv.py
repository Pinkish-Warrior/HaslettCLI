#!/usr/bin/env python3
"""
Simple starter CV CLI (Python + Click + Jinja2).
Commands:
  cv init
  cv add-profile PATH    # add a YAML profile into profiles/
  cv list
  cv generate --profile NAME --out out.html
"""
import os
import sys
import shutil
import json
import click
import yaml
from jinja2 import Environment, FileSystemLoader

BASE = os.path.abspath(os.path.dirname(__file__))

@click.group()
def cli():
    pass

@cli.command()
@click.argument("dest", default=".")
def init(dest):
    """Create project structure in DEST."""
    dest = os.path.abspath(dest)
    os.makedirs(os.path.join(dest, "templates"), exist_ok=True)
    os.makedirs(os.path.join(dest, "profiles"), exist_ok=True)
    # create a minimal jinja template
    tpl_path = os.path.join(dest, "templates", "cv_template.html.j2")
    if not os.path.exists(tpl_path):
        with open(tpl_path, "w") as f:
            f.write("""<!doctype html>
<html><head><meta charset="utf-8"><title>{{ person.name }} - CV</title></head>
<body>
  <h1>{{ person.name }}</h1>
  <p>{{ summary }}</p>
  <h2>Skills</h2><ul>{% for s in skills %}<li>{{ s }}</li>{% endfor %}</ul>
  <h2>Experience</h2>
  {% for e in experience %}
    <h3>{{ e.role }} — {{ e.company }}</h3>
    <ul>{% for b in e.bullets %}<li>{{ b }}</li>{% endfor %}</ul>
  {% endfor %}
</body></html>""")
    click.echo(f"Initialized cv project at {dest}")

@cli.command()
@click.argument("yaml_path", type=click.Path(exists=True))
def add_profile(yaml_path):
    """Copy YAML profile into ./profiles/"""
    profiles_dir = os.path.join(BASE, "profiles")
    os.makedirs(profiles_dir, exist_ok=True)
    name = os.path.basename(yaml_path)
    dest = os.path.join(profiles_dir, name)
    shutil.copy(yaml_path, dest)
    click.echo(f"Profile added: {dest}")

@cli.command()
def list_profiles():
    """List profiles in ./profiles"""
    profiles_dir = os.path.join(BASE, "profiles")
    if not os.path.isdir(profiles_dir):
        click.echo("No profiles found. Run `cv init` first.")
        return
    items = os.listdir(profiles_dir)
    for it in items:
        click.echo(f"- {it}")

@cli.command()
@click.option("--profile", required=True, help="profile filename in profiles/")
@click.option("--out", default="out.html", help="output HTML file")
def generate(profile, out):
    """Render profile -> HTML using templates/cv_template.html.j2"""
    profiles_dir = os.path.join(BASE, "profiles")
    tpl_dir = os.path.join(BASE, "templates")
    profile_path = os.path.join(profiles_dir, profile)
    if not os.path.exists(profile_path):
        click.echo("Profile not found.")
        sys.exit(1)
    with open(profile_path, "r") as f:
        data = yaml.safe_load(f)
    env = Environment(loader=FileSystemLoader(tpl_dir), autoescape=True)
    tpl = env.get_template("cv_template.html.j2")
    rendered = tpl.render(**data)
    with open(out, "w", encoding="utf-8") as f:
        f.write(rendered)
    click.echo(f"Wrote {out}")

if __name__ == "__main__":
    cli()