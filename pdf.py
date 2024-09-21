from fpdf import FPDF

EXPERIENCE_PANEL = 2

class ResumePDF(FPDF):
    def __init__(self, file_root: str):
        super().__init__(format="letter")
        self.file_root = file_root

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

    def add_header(self, resume):
        self.header_text(resume["name"])
        self.set_font("Helvetica", "", 9)
        self.set_y(31)
        self.cell(125, 9, resume["blurb"], align="L")
        self.ln()

    def add_experience(self, resume):
        self.section_header("Experience")
        for experience in resume["experience"][0:EXPERIENCE_PANEL]:
            self.three_part(
                experience["company"], experience["location"], experience["title"]
            )
            self.set_y(self.get_y() + 7)
            self.lesser_text()
            self.text_cell(experience["dates"])
            self.multi_cell(125, 5, experience["description"])

    def add_education(self, resume):
        self.section_header("Education")
        for education in resume["education"]:
            self.three_part(
                education["school"], education["location"], education["degree"]
            )
            self.set_y(self.get_y() + 7)
            self.lesser_text()
            self.text_cell(education["dates"])

    def add_additional_experience(self, resume):
        additional_experience = resume["experience"][EXPERIENCE_PANEL:]
        if not additional_experience:
            return
        self.section_header("Additional Work Experience")
        for experience in additional_experience:
            self.basic_bold()
            cell_width = self.get_string_width(experience["company"])
            self.cell(cell_width, 5, experience["company"])
            self.lesser_text()
            right = f" - {experience['location']} - {experience['title']} - {experience['dates']}"
            cell_width = self.get_string_width(right)
            self.cell(cell_width, 5, right)
            self.ln()

    def add_contact(self, resume):
        self.set_left_margin(150)
        self.set_y(15)
        self.basic_bold()
        self.text_cell(resume["phone"], height=5)
        self.text_cell(resume["email"], height=5)
        self.text_cell(resume["website"], height=5)
        self.text_cell(resume["address"], height=5)

    def add_skills(self, resume):
        self.set_y(45)
        self.section_header("Skills")
        self.lesser_text()
        for skill in resume["skills"]:
            self.text_cell(skill)

    def add_projects(self, resume):
        if not resume.get("projects"):
            return
        self.section_header("Projects")
        for project in resume["projects"]:
            self.basic_bold()
            self.text_cell(project["name"])
            self.lesser_text()
            self.multi_cell(50, 5, project["description"], align="L")
            self.ln()

    def write_file(self, resume):
        self.add_page()
        self.add_header(resume)
        self.add_experience(resume)
        self.add_additional_experience(resume)
        self.add_education(resume)
        self.add_contact(resume)
        self.add_skills(resume)
        self.add_projects(resume)
        self.output(f"{self.file_root}.pdf")
