from fpdf import FPDF

EXPERIENCE_PANEL = 2


class ResumePDF(FPDF):
    def __init__(self, file_root: str, longform: bool = False):
        super().__init__(format="letter")
        self.file_root = file_root
        self.longform = longform

    def basic_bold(self):
        self.set_text_color(0, 0, 0)
        self.set_font("Helvetica", "B", 9)

    def title_emphasis(self, style=""):
        self.set_font("Helvetica", style, 12)

    def header_text(self, text):
        self.set_font("Helvetica", "B", 36)
        self.cell(125, 31, text, align="L")

    def lesser_text(self, size=9):
        self.set_text_color(100, 100, 100)
        self.set_font("Helvetica", "", size)

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
        width = 190 if self.longform else 125
        self.cell(width, 9, resume["blurb"], align="L")
        self.ln()

    def add_experience(self, resume):
        self.section_header("Experience")
        experience_limit = None if self.longform else EXPERIENCE_PANEL
        width = 190 if self.longform else 125
        for experience in resume["experience"][0:experience_limit]:
            self.three_part(
                experience["company"], experience["location"], experience["title"]
            )
            self.set_y(self.get_y() + 7)
            body_size = 11 if self.longform else 9
            self.lesser_text(body_size)
            self.text_cell(experience["dates"])
            line_height = 6 if self.longform else 5
            self.multi_cell(width, line_height, experience["description"])

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
        if self.longform:
            return  # In longform, all experience is shown in detail
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
        if self.longform:
            return  # Don't show contact sidebar in longform
        if self.page_no() == 1:
            self.set_left_margin(150)
            self.set_y(15)
            self.basic_bold()
            self.text_cell(resume["phone"], height=5)
            self.text_cell(resume["email"], height=5)
            self.text_cell(resume["website"], height=5)
            self.text_cell(resume["address"], height=5)
            self.set_left_margin(10)  # Reset margin back

    def add_skills(self, resume):
        if self.longform:
            # In longform, skills are a full section in main content
            self.section_header("Skills")
            self.lesser_text(11)
            skills_text = " * ".join(resume["skills"])
            width = 190
            self.multi_cell(width, 6, skills_text)
        elif self.page_no() == 1:
            # In short form, skills are in the sidebar
            self.set_left_margin(150)
            self.set_y(45)
            self.section_header("Skills")
            self.lesser_text()
            for skill in resume["skills"]:
                self.text_cell(skill)
            self.set_left_margin(10)  # Reset margin back

    def add_projects(self, resume):
        if self.longform or not resume.get("projects"):
            return  # Don't show projects in longform
        if self.page_no() == 1:
            self.set_left_margin(150)
            self.section_header("Projects")
            for project in resume["projects"]:
                self.basic_bold()
                self.text_cell(project["name"])
                self.lesser_text()
                self.multi_cell(50, 5, project["description"], align="L")
                self.ln()
            self.set_left_margin(10)  # Reset margin back

    def write_file(self, resume):
        self.add_page()
        self.add_header(resume)
        self.add_experience(resume)
        self.add_additional_experience(resume)
        if self.longform:
            self.add_education(resume)
            self.add_skills(resume)
        else:
            self.add_education(resume)
            self.add_contact(resume)
            self.add_skills(resume)
            self.add_projects(resume)
        suffix = "-longform" if self.longform else ""
        self.output(f"{self.file_root}{suffix}.pdf")
