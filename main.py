import sys

import yaml

from pdf import ResumePDF


def write_resumes(file_root):
    with open("resume.yml", "r") as resume_file:
        resume = yaml.safe_load(resume_file)
        ResumePDF(file_root).write_file(resume)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("main.py <resume root name>")
        exit(-1)
    write_resumes(sys.argv[1])
