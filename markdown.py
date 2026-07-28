import yaml

class ResumeMarkdown:
    def __init__(self, file_root: str):
        self.file_root = file_root

    def write_file(self, resume):
        with open(f"{self.file_root}.md", "w") as f:
            f.write(f"# {resume['name']}\n\n")
            f.write(f"{resume['email']} | {resume['phone']} | {resume['address']} | {resume['website']}\n\n")
            f.write(f"{resume['blurb']}\n\n")
            
            if 'extended_blurb' in resume:
                f.write("## Professional Summary\n\n")
                f.write(f"{resume['extended_blurb']}\n\n")
            
            f.write("## Experience\n\n")
            for exp in resume['experience']:
                f.write(f"### {exp['title']} at {exp['company']}\n")
                f.write(f"{exp['dates']} | {exp['location']}\n\n")
                description = exp['description']
                # Clean up description
                if isinstance(description, list):
                    for item in description:
                        f.write(f"- {item}\n")
                else:
                    lines = description.strip().split('\n')
                    for line in lines:
                        line = line.strip()
                        if line.startswith('* '):
                            f.write(f"- {line[2:]}\n")
                        else:
                            f.write(f"{line}\n")
                f.write("\n")
            
            f.write("## Education\n\n")
            for edu in resume['education']:
                f.write(f"- **{edu['school']}**: {edu['degree']} ({edu['dates']})\n")
            f.write("\n")
            
            f.write("## Skills\n\n")
            for skill in resume['skills']:
                f.write(f"- {skill}\n")
            f.write("\n")
