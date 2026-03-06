# Andrew's Resume

This is my resume generator.  I update `resume.yml` and github actions runs the python script which generates a PDF resume similar in style to Google Doc's default resume template.

My most current resume can be downloaded by clicking [here](https://github.com/aviolette/resume/releases/latest) and downloading AJVResume.pdf.

## Setup

This project uses [uv](https://docs.astral.sh/uv/) for dependency management and Python 3.13.

```bash
# Install dependencies
uv sync

# Run the resume generator
uv run python main.py <resume_root_name>
```
