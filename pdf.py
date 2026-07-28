from fpdf import FPDF

EXPERIENCE_PANEL = 2


class ResumePDF(FPDF):
    def __init__(self, file_root: str):
        super().__init__(format="letter")
        self.file_root = file_root
        # Add DejaVu Sans font which supports Unicode
        self.add_font("DejaVu", "", "fonts/DejaVuSans.ttf", uni=True)
        self.add_font("DejaVu", "B", "fonts/DejaVuSans-Bold.ttf", uni=True)
        self.add_font("DejaVu", "I", "fonts/DejaVuSans-Oblique.ttf", uni=True)

    def basic_bold(self):
        self.set_text_color(0, 0, 0)
        self.set_font("DejaVu", "B", 9)

    def title_emphasis(self, style=""):
        self.set_font("DejaVu", style, 12)

    def header_text(self, text):
        self.set_font("DejaVu", "B", 36)
        self.cell(125, 31, text, align="L")

    def lesser_text(self, size=9):
        self.set_text_color(100, 100, 100)
        self.set_font("DejaVu", "", size)

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

    def render_description(self, description, width, line_height):
        """Render description text, handling list of strings or markdown-style bullet lists."""
        if isinstance(description, list):
            bullets = description
        elif ' * ' in description or description.strip().startswith('* '):
            # Split on bullet markers, handling both patterns
            parts = description.split(' * ')
            bullets = []

            # First part might be empty or have leading bullet
            first = parts[0].strip()
            if first.startswith('* '):
                bullets.append(first[2:].strip())
            elif first:
                bullets.append(first)

            # Rest of the parts are bullets
            for part in parts[1:]:
                if part.strip():
                    bullets.append(part.strip())
        else:
            # No bullets, render as normal
            self.multi_cell(width, line_height, description)
            return

        # Render each bullet
        x_pos = self.get_x()
        for bullet in bullets:
            if bullet:
                # Use proper Unicode bullet character (•)
                self.cell(3, line_height, '•')
                self.set_x(x_pos + 5)
                self.multi_cell(width - 5, line_height, bullet)
                self.set_x(x_pos)

    def add_header(self, resume):
        self.header_text(resume["name"])
        self.set_font("Helvetica", "", 9)
        self.set_y(31)
        width = 190
        self.cell(width, 9, resume["blurb"], align="L")
        self.ln()

    def add_professional_summary(self, resume):
        if "extended_blurb" not in resume:
            return
        self.section_header("Professional Summary")
        self.lesser_text(11)
        self.multi_cell(190, 6, resume["extended_blurb"])

    def add_experience(self, resume):
        self.section_header("Experience")
        width = 190
        for experience in resume["experience"]:
            self.three_part(
                experience["company"], experience["location"], experience["title"]
            )
            self.set_y(self.get_y() + 7)
            body_size = 11
            self.lesser_text(body_size)
            self.text_cell(experience["dates"])
            line_height = 6
            self.render_description(experience["description"], width, line_height)

    def add_education(self, resume):
        self.section_header("Education")
        for education in resume["education"]:
            self.three_part(
                education["school"], education["location"], education["degree"]
            )
            self.set_y(self.get_y() + 7)
            self.lesser_text()
            self.text_cell(education["dates"])

    def add_contact(self, resume):
        if self.page_no() == 1:
            self.set_left_margin(150)
            self.set_y(20)
            self.basic_bold()
            self.text_cell(resume["phone"], height=5)
            self.text_cell(resume["email"], height=5)
            self.text_cell(resume["website"], height=5)
            self.text_cell(resume["address"], height=5)
            self.set_left_margin(10)  # Reset margin back

    def add_skills(self, resume):
        self.section_header("Skills")
        self.lesser_text(11)
        self.render_description(resume["skills"], 190, 6)

    def add_projects(self, resume):
        pass # Projects are not supported in this version

    def write_file(self, resume):
        self.add_page()
        self.add_header(resume)
        self.add_contact(resume)
        self.add_professional_summary(resume)
        self.add_experience(resume)
        self.add_education(resume)
        self.add_skills(resume)
        self.output(f"{self.file_root}.pdf")
