# Next Step: Integrate Job Search Feature

This document outlines the plan to integrate a job search feature into HaslettCLI.

## 1. API Choice

We will use the **Arbeitnow API** for the initial implementation.

- **Reasoning:** It is free, does not require an API key, and has a focus on technology jobs. This makes it ideal for rapid prototyping.
- **API Documentation:** [https://arbeitnow.com/api/job-board-api](https://arbeitnow.com/api/job-board-api)

## 2. Implementation Plan

### Step 2.1: Add New Dependency

- We will add the `requests` library to the project to handle HTTP requests to the API.
- This involves:
  - Appending `requests` to `requirements.txt`.
  - Running `pip install -r requirements.txt`.

### Step 2.2: Create API Client

- A new file, `api_client.py`, will be created.
- This file will contain a function, `search_jobs(description, location, etc.)`, responsible for querying the Arbeitnow API and returning structured job data.

### Step 2.3: Add New CLI Command

- A new `search` command will be added to `haslettcli.py`.
- The command will accept options to filter the search, for example:

  ```bash
  ./run.sh search --description "Python Developer" --location "USA"
  ```

### Step 2.4: Display Results

- The `search` command will call the `search_jobs` function from the API client.
- It will then loop through the results and print them to the console in a clean, readable format (e.g., "Job Title at Company - Location").
