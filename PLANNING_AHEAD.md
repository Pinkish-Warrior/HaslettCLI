# Planning Ahead: Project Evolution

This document outlines the next steps for the HaslettCLI project, focusing on two key areas: creating robust user profiles and integrating with a job advertising API.

## 1. Building Strong User Profiles

The goal is to create detailed and effective user profiles that can be used to generate compelling CVs and cover letters.

### Steps

1. **Define Profile Schema:**
    * Determine the necessary fields for a comprehensive professional profile. This should include:
        * Personal Details (Name, Contact Info, Professional Title)
        * Summary/Bio
        * Work Experience (Company, Role, Dates, Responsibilities, Achievements)
        * Education (Institution, Degree, Dates)
        * Skills (Technical, Soft Skills)
        * Projects/Portfolio
        * Certifications/Awards
        * Social/Professional Links (LinkedIn, GitHub, etc.)
        * Decide on a structured format for storing this data (e.g., YAML, JSON). We have chosen YAML for its human-readability and suitability for complex data structures.
        * **Pros of YAML**: It is easy for users to read and edit, supports complex nested data, and is generally more concise than alternatives like XML.
        * **Cons and Mitigation**: The main drawback of YAML is a security risk that allows for arbitrary code execution from untrusted files. To counter this, we will strictly use the `yaml.safe_load()` function from the `PyYAML` library. This function only parses basic data types (strings, numbers, lists, dictionaries) and prevents any code execution, making it a secure choice for handling profile data.

2. **Implement Profile Management:**
    * Create CLI commands to manage profiles:
        * `haslettcli profile create`: To create a new profile from scratch or from a template.
        * `haslettcli profile edit`: To update an existing profile.
        * `haslettcli profile view`: To display the current profile information.
        * `haslettcli profile list`: To list all available profiles.
    * The `profile.example.yml` can be used as a base template.

3. **Enhance CV/Cover Letter Generation:**
    * Update the Jinja2 templates (`cv_template.html.j2`, `cover_template.txt.j2`) to use the new detailed profile schema.
    * Add logic to selectively include or exclude sections of the profile in the generated documents, allowing for tailored applications.

## 2. API Integration for Job Advertising

The aim is to connect HaslettCLI with a job advertising platform to fetch job descriptions and use them to tailor CVs and cover letters.

### Further Steps

1. **Research Job APIs:**
    * Investigate available job board APIs. Potential candidates include:
        * Reed
        * Adzuna
        * Indeed
        * LinkedIn (may have limitations)
    * Evaluate APIs based on ease of use, data quality, and authentication requirements.

2. **Design the Integration:**
    * Define the workflow for using the API. A likely scenario:
        1. User searches for jobs using a command (e.g., `haslettcli jobs search --keyword "Python Developer" --location "London"`).
        2. The CLI calls the chosen job API to get a list of jobs.
        3. The user can then select a job to view more details.
        4. The job details (especially the description) are used to pre-fill or suggest keywords for a cover letter or CV.

3. **Implement the API Client:**
    * Create a new module in the `utils` directory for the API client (e.g., `job_api_client.py`).
    * This module will handle making requests to the job API and parsing the responses.
    * API keys and other sensitive information should be managed through environment variables or a configuration file.

4. **Create New CLI Commands:**
    * Add new commands to `haslettcli.py` for interacting with the job API:
        * `haslettcli jobssearch`: To search for jobs.
        * `haslettcli jobs view <job_id>`: To view the details of a specific job.
        * `haslettcli apply <job_id>`: A command that could orchestrate the process of tailoring a CV and cover letter for a specific job.

## Timeline and Priorities

1. ✅ **Priority 1 (Short-Term):** Implement the profile management features. A solid profile structure is the foundation for the rest of the project.
2. 🔄 **Priority 2 (Mid-Term):** Begin research and initial implementation of the API integration. This can start with a simple client that can fetch and display job listings.
3. 🔜 **Priority 3 (Long-Term):** Fully integrate the job data with the CV and cover letter generation process, providing an end-to-end application tailoring experience.

---

## Legend for Task Status

| Symbol |               Status              |
| :----: | :---------------------------------|
|   ✅   | **Actioned / Completed**          |
|   🔄   | **In Progress**                   |
|   🔜   | **Pending / Not Yet In Progress** |
