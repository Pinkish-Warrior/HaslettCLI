#!/usr/bin/env python3
"""
HaslettCLI: CLI tool for CV and cover letter generation with PDF support.
"""
import os
import shutil
import click
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

from utils import load_profile_data

BASE = os.path.abspath(os.path.dirname(__file__))

@click.group()
def cli():
    """A CLI tool for CV and cover letter generation."""

# ---------------- Init ----------------
@cli.command()
def init():
    """Initialize project structure."""
    os.makedirs(os.path.join(BASE, "templates"), exist_ok=True)
    os.makedirs(os.path.join(BASE, "profiles"), exist_ok=True)
    click.echo(f"Initialized project at {BASE}")

# ---------------- Profile Management ----------------
@click.group()
def profile():
    """Manage user profiles."""

cli.add_command(profile)

@profile.command()
@click.argument("name")
def create(name):
    """Create a new profile from the example."""
    profiles_dir = os.path.join(BASE, "profiles")
    os.makedirs(profiles_dir, exist_ok=True)
    example_profile_path = os.path.join(BASE, "profile.example.yml")
    new_profile_path = os.path.join(profiles_dir, f"{name}.yml")

    if not os.path.exists(example_profile_path):
        click.echo("Error: profile.example.yml not found.")
        return

    if os.path.exists(new_profile_path):
        click.echo(f"Error: Profile '{name}.yml' already exists.")
        return

    shutil.copy(example_profile_path, new_profile_path)
    click.echo(f"Profile '{name}.yml' created in {profiles_dir}")


@profile.command()
@click.argument("yaml_path", type=click.Path(exists=True))
def add(yaml_path):
    """Add YAML profile from an existing file and remove the original."""
    profiles_dir = os.path.join(BASE, "profiles")
    os.makedirs(profiles_dir, exist_ok=True)
    name = os.path.basename(yaml_path)
    destination_path = os.path.join(profiles_dir, name)

    if os.path.exists(destination_path):
        click.echo(f"Error: Profile '{name}' already exists in profiles directory.")
        return

    shutil.copy(yaml_path, destination_path)
    os.remove(yaml_path)  # Remove the original file
    click.echo(f"Profile '{name}' added and original file removed.")


@profile.command(name="list")
def list_profiles():
    """List all profiles."""
    profiles_dir = os.path.join(BASE, "profiles")
    if not os.path.isdir(profiles_dir):
        click.echo("No profiles found. Run `init` first.")
        return
    for f in os.listdir(profiles_dir):
        click.echo(f"- {f}")

# ---------------- Generate CV ----------------
@cli.command()
@click.option("--profile", "profile_name", required=True, help="Profile YAML file")
@click.option("--out", default="out.pdf", help="Output file")
@click.option("--format", "format_", type=click.Choice(["html", "pdf"]), default="pdf")
@click.option("--template", default="cv_template.html.j2")
def generate(profile_name, out, format_, template):
    """Render CV."""
    profiles_dir = os.path.join(BASE, "profiles")
    tpl_dir = os.path.join(BASE, "templates")
    output_dir = os.path.join(BASE, "output")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, out)

    data = load_profile_data(profile_name, profiles_dir)

    env = Environment(loader=FileSystemLoader(tpl_dir), autoescape=True)
    tpl = env.get_template(template)
    rendered = tpl.render(**data)

    if format_ == "html":
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(rendered)
        click.echo(f"HTML CV written to {output_path}")
    else:
        HTML(string=rendered).write_pdf(output_path)
        click.echo(f"PDF CV written to {output_path}")

# ---------------- Generate Cover Letter ----------------
@cli.command()
@click.option("--profile", "profile_name", required=True)
@click.option("--job", required=True, help="Job title / company")
@click.option("--out", default="cover.pdf")
@click.option("--format", "format_", type=click.Choice(["txt", "pdf"]), default="pdf")
@click.option("--template", default="cover_template.txt.j2")
def cover(profile_name, job, out, format_, template):
    """Generate cover letter."""
    profiles_dir = os.path.join(BASE, "profiles")
    tpl_dir = os.path.join(BASE, "templates")
    output_dir = os.path.join(BASE, "output")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, out)

    data = load_profile_data(profile_name, profiles_dir)
    data["job"] = job

    env = Environment(loader=FileSystemLoader(tpl_dir), autoescape=True)
    tpl = env.get_template(template)
    rendered = tpl.render(**data)

    if format_ == "txt":
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(rendered)
    else:
        HTML(string=rendered).write_pdf(output_path)

    click.echo(f"Cover letter written to {output_path}")

if __name__ == "__main__":
    cli()
