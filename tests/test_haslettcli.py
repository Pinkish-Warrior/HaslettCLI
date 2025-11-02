"""
Tests for the HaslettCLI tool.
"""
import os
import subprocess
import yaml

# Get the absolute path to the root of the project
# This allows tests to be run from anywhere
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
RUN_SCRIPT = os.path.join(PROJECT_ROOT, 'run.sh')


def test_init(tmp_path):
    """
    Tests the 'init' command in a temporary directory.
    """
    # Run the init command inside the temporary directory
    result = subprocess.run(
        [RUN_SCRIPT, "init"], cwd=tmp_path, capture_output=True, text=True, check=True
    )

    # Check that the command ran successfully
    assert result.returncode == 0
    assert "Initialized project" in result.stdout

    # Check that the directories were created
    assert (tmp_path / "templates").is_dir()
    assert (tmp_path / "profiles").is_dir()


def test_add_and_list_profile(tmp_path):
    """
    Tests adding and listing a profile.
    """
    # First, initialize a project in the temp directory
    subprocess.run([RUN_SCRIPT, "init"], cwd=tmp_path, check=True)

    # Create a dummy profile file inside the temp directory
    dummy_profile_content = {
        "person": {"name": "Test User"},
        "summary": "Test summary."
    }
    dummy_profile_path = tmp_path / "dummy_profile.yml"
    with open(dummy_profile_path, 'w', encoding="utf-8") as f:
        yaml.dump(dummy_profile_content, f)

    # Run the 'add-profile' command
    add_result = subprocess.run(
        [RUN_SCRIPT, "add-profile", str(dummy_profile_path)],
        cwd=tmp_path, capture_output=True, text=True, check=True
    )

    assert add_result.returncode == 0
    assert "Profile added: dummy_profile.yml" in add_result.stdout

    # Check that the profile was copied into the 'profiles' directory
    assert (tmp_path / "profiles" / "dummy_profile.yml").exists()

    # Run the 'list-profiles' command
    list_result = subprocess.run(
        [RUN_SCRIPT, "list-profiles"], cwd=tmp_path, capture_output=True, text=True, check=True
    )

    assert list_result.returncode == 0
    assert "dummy_profile.yml" in list_result.stdout


def test_generate_and_cover(tmp_path):
    """
    Tests the 'generate' and 'cover' commands.
    """
    # Initialize project. This creates the profiles and templates dirs.
    subprocess.run([RUN_SCRIPT, "init"], cwd=tmp_path, check=True)

    # Copy the real templates into the temp test environment's 'templates' dir
    templates_dir = tmp_path / "templates"
    project_templates_dir = os.path.join(PROJECT_ROOT, 'templates')

    # Copy cv_template.html.j2
    subprocess.run(
        ["cp", os.path.join(project_templates_dir, "cv_template.html.j2"), templates_dir],
        check=True
    )
    # Copy cover_template.txt.j2
    subprocess.run(
        ["cp", os.path.join(project_templates_dir, "cover_template.txt.j2"), templates_dir],
        check=True
    )

    # Create and add a full dummy profile
    dummy_profile_path = tmp_path / "dummy_profile.yml"
    dummy_profile_content = {
        "person": {
            "name": "Jane Doe", "email": "j@d.com", "phone": "123",
            "linkedin": "linkedin.com/in/janedoe", "github": "github.com/janedoe"
        },
        "summary": "A passionate software engineer.",
        "skills": ["Python", "Testing"],
        "experience": [{
            "role": "Engineer", "company": "TestCo", "period": "2023-Present",
            "bullets": ["Wrote tests."]
        }]
    }
    with open(dummy_profile_path, 'w', encoding="utf-8") as f:
        yaml.dump(dummy_profile_content, f)
    subprocess.run(
        [RUN_SCRIPT, "add-profile", str(dummy_profile_path)], cwd=tmp_path, check=True
    )

    # Test 'generate'
    generate_result = subprocess.run(
        [RUN_SCRIPT, "generate", "--profile", "dummy_profile.yml", "--out", "cv.pdf"],
        cwd=tmp_path, capture_output=True, text=True, check=True
    )
    assert generate_result.returncode == 0
    assert "PDF CV written to cv.pdf" in generate_result.stdout
    assert (tmp_path / "cv.pdf").exists()

    # Test 'cover'
    cover_result = subprocess.run(
        [
            RUN_SCRIPT, "cover", "--profile", "dummy_profile.yml",
            "--job", "TestCo", "--out", "cover.pdf"
        ],
        cwd=tmp_path, capture_output=True, text=True, check=True
    )
    assert cover_result.returncode == 0
    assert "Cover letter written to cover.pdf" in cover_result.stdout
    assert (tmp_path / "cover.pdf").exists()
