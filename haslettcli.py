#!/usr/bin/env python3
"""
HaslettCLI: CLI tool for CV and cover letter generation with PDF support.
"""
import os
import sys
import shutil
import click
import yaml
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

BASE = os.path.abspath(os.path.dirname(__file__))

@click.group()
def cli():
    pass

# ---------------- Init ----------------
@cli.command()
@click.argument("dest", default=".")
def init(dest):
    """Initialize project structure."""
    dest = os.path.abspath(dest)
    os.makedirs(os.path.join(dest, "templates"), exist_ok=True)
    os.makedirs(os.path.join(dest, "profiles"), exist_ok=True)
    click.echo(f"Initialized project at {dest}")

# ---------------- Add Profile ----------------
@cli.command()
@click.argument("yaml_path", type=click.Path(exists=True))
def add_profile(yaml_path):
    """Add YAML profile."""
    profiles_dir = os.path.join(os.getcwd(), "profiles")
    os.makedirs(profiles_dir, exist_ok=True)
    name = os.path.basename(yaml_path)
    shutil.copy(yaml_path, os.path.join(profiles_dir, name))
    click.echo(f"Profile added: {name}")

# ---------------- List Profiles ----------------
@cli.command()
def list_profiles():
    """List all profiles."""
    profiles_dir = os.path.join(os.getcwd(), "profiles")
    if not os.path.isdir(profiles_dir):
        click.echo("No profiles found. Run `init` first.")
        return
    for f in os.listdir(profiles_dir):
        click.echo(f"- {f}")

# ---------------- Generate CV ----------------
@cli.command()
@click.option("--profile", required=True, help="Profile YAML file")
@click.option("--out", default="out.pdf", help="Output file")
@click.option("--format", type=click.Choice(["html", "pdf"]), default="pdf")
@click.option("--template", default="cv_template.html.j2")
def generate(profile, out, format, template):
    """Render CV."""
    profiles_dir = os.path.join(os.getcwd(), "profiles")
    tpl_dir = os.path.join(BASE, "templates")
    profile_path = os.path.join(profiles_dir, profile)
    if not os.path.exists(profile_path):
        click.echo("Profile not found.")
        sys.exit(1)

    with open(profile_path, "r") as f:
        data = yaml.safe_load(f)

    env = Environment(loader=FileSystemLoader(tpl_dir), autoescape=True)
    tpl = env.get_template(template)
    rendered = tpl.render(**data)

    if format == "html":
        with open(out, "w", encoding="utf-8") as f:
            f.write(rendered)
        click.echo(f"HTML CV written to {out}")
    else:
        HTML(string=rendered).write_pdf(out)
        click.echo(f"PDF CV written to {out}")

# ---------------- Generate Cover Letter ----------------
@cli.command()
@click.option("--profile", required=True)
@click.option("--job", required=True, help="Job title / company")
@click.option("--out", default="cover.pdf")
@click.option("--format", type=click.Choice(["txt", "pdf"]), default="pdf")
@click.option("--template", default="cover_template.txt.j2")
def cover(profile, job, out, format, template):
    """Generate cover letter."""
    profiles_dir = os.path.join(os.getcwd(), "profiles")
    tpl_dir = os.path.join(BASE, "templates")
    profile_path = os.path.join(profiles_dir, profile)
    if not os.path.exists(profile_path):
        click.echo("Profile not found.")
        sys.exit(1)

    with open(profile_path, "r") as f:
        data = yaml.safe_load(f)
    data["job"] = job

    env = Environment(loader=FileSystemLoader(tpl_dir), autoescape=True)
    tpl = env.get_template(template)
    rendered = tpl.render(**data)

    if format == "txt":
        with open(out, "w", encoding="utf-8") as f:
            f.write(rendered)
    else:
        HTML(string=rendered).write_pdf(out)

    click.echo(f"Cover letter written to {out}")

if __name__ == "__main__":
    cli()