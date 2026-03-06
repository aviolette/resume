import sys

import yaml

from pdf import ResumePDF


def write_resumes(file_root):
    with open("resume.yml", "r") as resume_file:
        resume = yaml.safe_load(resume_file)
        # Generate short form
        ResumePDF(file_root, longform=False).write_file(resume)
        # Generate long form
        ResumePDF(file_root, longform=True).write_file(resume)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("main.py <resume root name>")
        exit(-1)
    write_resumes(sys.argv[1])
