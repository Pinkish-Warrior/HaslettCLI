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

def test_init():
    """
    Tests the 'init' command.
    """
    # Run the init command
    result = subprocess.run(
        [RUN_SCRIPT, "init"], capture_output=True, text=True, check=True
    )

    # Check that the command ran successfully
    assert result.returncode == 0
    assert "Initialized project" in result.stdout

def test_profile_create(tmp_path):
    """
    Tests the 'profile create' command.
    """
    profile_name = "test_create_profile"
    profile_file = f"{profile_name}.yml"
    profiles_dir = os.path.join(PROJECT_ROOT, 'profiles')
    profile_path = os.path.join(profiles_dir, profile_file)

    # Ensure the profile doesn't exist before the test
    if os.path.exists(profile_path):
        os.remove(profile_path)

    # Run the 'profile create' command
    result = subprocess.run(
        [RUN_SCRIPT, "profile", "create", profile_name],
        capture_output=True, text=True, check=True
    )

    assert result.returncode == 0
    assert f"Profile '{profile_file}' created" in result.stdout
    assert os.path.exists(profile_path)

    # Clean up the created profile
    os.remove(profile_path)

def test_profile_add_and_list(tmp_path):
    """
    Tests 'profile add' and 'profile list' commands.
    """
    # Create a dummy profile file in the temp directory
    dummy_profile_content = {"summary": "Test summary."}
    dummy_profile_path = tmp_path / "dummy_add_profile.yml"
    with open(dummy_profile_path, 'w', encoding="utf-8") as f:
        yaml.dump(dummy_profile_content, f)

    # Run the 'profile add' command
    add_result = subprocess.run(
        [RUN_SCRIPT, "profile", "add", str(dummy_profile_path)],
        capture_output=True, text=True, check=True
    )

    assert add_result.returncode == 0
    assert "Profile 'dummy_add_profile.yml' added" in add_result.stdout

    # Check that the profile was copied into the project's 'profiles' directory
    profiles_dir = os.path.join(PROJECT_ROOT, 'profiles')
    added_profile_path = os.path.join(profiles_dir, "dummy_add_profile.yml")
    assert os.path.exists(added_profile_path)

    # Run the 'profile list' command
    list_result = subprocess.run(
        [RUN_SCRIPT, "profile", "list"],
        capture_output=True, text=True, check=True
    )

    assert list_result.returncode == 0
    assert "dummy_add_profile.yml" in list_result.stdout

    # Clean up
    os.remove(added_profile_path)

def test_profile_add_removes_original(tmp_path):
    """
    Tests that 'profile add' removes the original file.
    """
    # Create a dummy profile file in the temp directory
    dummy_profile_content = {"summary": "Test summary."}
    dummy_profile_path = tmp_path / "dummy_remove_profile.yml"
    with open(dummy_profile_path, 'w', encoding="utf-8") as f:
        yaml.dump(dummy_profile_content, f)

    # Run the 'profile add' command
    subprocess.run(
        [RUN_SCRIPT, "profile", "add", str(dummy_profile_path)],
        check=True
    )

    # Check that the original file was removed
    assert not os.path.exists(dummy_profile_path)

    # Clean up the added profile
    profiles_dir = os.path.join(PROJECT_ROOT, 'profiles')
    added_profile_path = os.path.join(profiles_dir, "dummy_remove_profile.yml")
    if os.path.exists(added_profile_path):
        os.remove(added_profile_path)

def test_generate_cv(tmp_path):
    """
    Tests the 'generate' command with the new profile schema.
    """
    # Create a full dummy profile using the new schema
    profile_name = "test_generate_profile"
    profile_file = f"{profile_name}.yml"
    profiles_dir = os.path.join(PROJECT_ROOT, 'profiles')
    profile_path = os.path.join(profiles_dir, profile_file)

    dummy_profile_content = {
        "personal_details": {
            "name": "Jane Doe",
            "professional_title": "Software Engineer",
            "email": "jane.doe@example.com",
            "phone": "123-456-7890",
            "social_links": {
                "linkedin": "linkedin.com/in/janedoe",
                "github": "github.com/janedoe",
                "portfolio": "janedoe.com"
            }
        },
        "summary": "A passionate software engineer.",
        "skills": {
            "technical": ["Python", "Testing"],
            "soft_skills": ["Teamwork"]
        },
        "work_experience": [{
            "role": "Engineer", "company": "TestCo", "period": "2023-Present",
            "responsibilities": ["Wrote tests."],
            "achievements": ["Achieved 100% test coverage."]
        }],
        "education": [{
            "institution": "Test University",
            "degree": "B.S. in Testing",
            "period": "2019-2023"
        }],
        "projects": [{
            "name": "Testing Framework",
            "description": "A framework for testing things.",
            "technologies": ["Python", "pytest"],
            "link": "github.com/janedoe/testing-framework"
        }],
        "certifications_awards": [{
            "name": "Certified Tester",
            "issuer": "Test Institute",
            "year": "2023"
        }]
    }
    with open(profile_path, 'w', encoding="utf-8") as f:
        yaml.dump(dummy_profile_content, f)

    # Test 'generate' for PDF
    pdf_out_file = "cv.pdf"
    generate_result_pdf = subprocess.run(
        [RUN_SCRIPT, "generate", "--profile", profile_file, "--out", pdf_out_file],
        capture_output=True, text=True, check=True
    )
    
    output_dir = os.path.join(PROJECT_ROOT, 'output')
    pdf_output_path = os.path.join(output_dir, pdf_out_file)

    assert generate_result_pdf.returncode == 0
    assert f"PDF CV written to {pdf_output_path}" in generate_result_pdf.stdout
    assert os.path.exists(pdf_output_path)

    # Test 'generate' for HTML
    html_out_file = "cv.html"
    generate_result_html = subprocess.run(
        [RUN_SCRIPT, "generate", "--profile", profile_file, "--out", html_out_file, "--format", "html"],
        capture_output=True, text=True, check=True
    )
    
    html_output_path = os.path.join(output_dir, html_out_file)

    assert generate_result_html.returncode == 0
    assert f"HTML CV written to {html_output_path}" in generate_result_html.stdout
    assert os.path.exists(html_output_path)

    # Clean up
    os.remove(profile_path)
    os.remove(pdf_output_path)
    os.remove(html_output_path)

def test_generate_cover_letter(tmp_path):
    """
    Tests the 'cover' command with the new profile schema.
    """
    # Create a full dummy profile using the new schema
    profile_name = "test_cover_profile"
    profile_file = f"{profile_name}.yml"
    profiles_dir = os.path.join(PROJECT_ROOT, 'profiles')
    profile_path = os.path.join(profiles_dir, profile_file)

    dummy_profile_content = {
        "personal_details": {
            "name": "John Doe",
            "professional_title": "Product Manager",
            "email": "john.doe@example.com",
            "phone": "555-555-5555",
        },
        "summary": "An experienced product manager.",
        "skills": {
            "technical": ["Agile", "Scrum"],
            "soft_skills": ["Leadership"]
        },
        "work_experience": [{
            "role": "Senior Product Manager",
            "company": "Big Tech",
            "period": "2020-Present",
            "responsibilities": ["Led product team.", "Defined product roadmap."],
            "achievements": ["Launched new feature.", "Increased user engagement."]
        }],
    }
    with open(profile_path, 'w', encoding="utf-8") as f:
        yaml.dump(dummy_profile_content, f)

    # Test 'cover' for txt
    txt_out_file = "cover.txt"
    job_title = "Product Owner"
    cover_result_txt = subprocess.run(
        [RUN_SCRIPT, "cover", "--profile", profile_file, "--job", job_title, "--out", txt_out_file, "--format", "txt"],
        capture_output=True, text=True, check=True
    )
    
    output_dir = os.path.join(PROJECT_ROOT, 'output')
    txt_output_path = os.path.join(output_dir, txt_out_file)

    assert cover_result_txt.returncode == 0
    assert f"Cover letter written to {txt_output_path}" in cover_result_txt.stdout
    assert os.path.exists(txt_output_path)

    # Check content of the generated file
    with open(txt_output_path, 'r', encoding="utf-8") as f:
        content = f.read()
        assert "John Doe" in content
        assert "Product Owner" in content
        assert "Senior Product Manager" in content

    # Clean up
    os.remove(profile_path)
    os.remove(txt_output_path)
