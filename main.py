import yaml
from fpdf import FPDF


class ResumePDF(FPDF):
    def __init__(self):
        super().__init__(format="letter")

    def basic_bold(self):
        self.set_text_color(0, 0, 0)
        self.set_font("Helvetica", "B", 9)

    def title_emphasis(self, style=""):
        self.set_font("Helvetica", style, 12)

    def header_text(self, text):
        self.set_font("Helvetica", "B", 36)
        self.cell(125, 31, text, align="L")

    def lesser_text(self):
        self.set_text_color(100, 100, 100)
        self.set_font("Helvetica", "", 9)

    def section_header(self, value):
        self.ln()
        self.basic_bold()
        self.set_text_color(31, 121, 199)
        self.cell(self.get_string_width(value), self.font_size_pt, value.upper())
        self.ln()

    def three_part(self, first, second, third):
        self.set_text_color(0, 0, 0)
        self.title_emphasis("B")
        cell_width = self.get_string_width(first)
        self.cell(cell_width, 12, first)
        self.title_emphasis("")
        middle = f", {second} - "
        cell_width = self.get_string_width(middle)
        self.cell(cell_width, 12, middle)
        self.title_emphasis("I")
        cell_width = self.get_string_width(third)
        self.cell(cell_width, 12, third)

    def text_cell(self, text, height=None, lf=True):
        self.cell(
            self.get_string_width(text), height if height else self.font_size_pt, text
        )
        if lf:
            self.ln()


def convert_resume():
    pdf = ResumePDF()
    with open("resume.yml", "r") as resume_file:
        resume = yaml.safe_load(resume_file)
        pdf.add_page()
        _add_header(resume, pdf)
        _add_experience(resume, pdf)
        _add_additional_experience(resume, pdf)
        _add_education(resume, pdf)
        _add_contact(resume, pdf)
        _add_skills(resume, pdf)
        _add_projects(resume, pdf)
    pdf.output("AJVResume.pdf", "F")


def _add_header(resume, pdf):
    pdf.header_text(resume["name"])
    pdf.set_font("Helvetica", "", 9)
    pdf.set_y(31)
    pdf.cell(125, 9, resume["blurb"], align="L")
    pdf.ln()


def _add_experience(resume, pdf):
    pdf.section_header("Experience")
    for experience in resume["experience"][0:3]:
        pdf.three_part(
            experience["company"], experience["location"], experience["title"]
        )
        pdf.set_y(pdf.get_y() + 7)
        pdf.lesser_text()
        pdf.text_cell(experience["dates"])
        pdf.multi_cell(125, 5, experience["description"])


def _add_additional_experience(resume, pdf):
    additional_experience = resume["experience"][3:]
    if not additional_experience:
        return
    pdf.section_header("Additional Work Experience")
    for experience in additional_experience:
        pdf.basic_bold()
        cell_width = pdf.get_string_width(experience["company"])
        pdf.cell(cell_width, 5, experience["company"])
        pdf.lesser_text()
        right = f" - {experience['location']} - {experience['title']} - {experience['dates']}"
        cell_width = pdf.get_string_width(right)
        pdf.cell(cell_width, 5, right)
        pdf.ln()


def _add_education(resume, pdf):
    pdf.section_header("Education")
    for education in resume["education"]:
        pdf.three_part(education["school"], education["location"], education["degree"])
        pdf.set_y(pdf.get_y() + 7)
        pdf.lesser_text()
        pdf.text_cell(education["dates"])


def _add_contact(resume, pdf):
    pdf.set_left_margin(150)
    pdf.set_y(15)
    pdf.basic_bold()
    pdf.text_cell(resume["phone"], height=5)
    pdf.text_cell(resume["email"], height=5)
    pdf.text_cell(resume["website"], height=5)
    pdf.text_cell(resume["address"], height=5)


def _add_skills(resume, pdf):
    pdf.set_y(45)
    pdf.section_header("Skills")
    pdf.lesser_text()
    for skill in resume["skills"]:
        pdf.text_cell(skill)


def _add_projects(resume, pdf):
    if not resume.get("projects"):
        return
    pdf.section_header("Projects")
    for project in resume["projects"]:
        pdf.basic_bold()
        pdf.text_cell(project["name"])
        pdf.lesser_text()
        pdf.multi_cell(50, 5, project["description"], align="L")
        pdf.ln()


if __name__ == "__main__":
    convert_resume()
