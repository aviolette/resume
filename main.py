import yaml
from fpdf import FPDF


def _add_header(resume_config, pdf, style):
    headline_font_size = style["headline_font_size"]
    pdf.set_font("Helvetica", "B", headline_font_size)
    pdf.cell(
        style["left_column"], headline_font_size - 5, resume_config["name"], align="L"
    )
    pdf.set_font("Helvetica", "", 9)
    pdf.set_y(headline_font_size - 5)
    pdf.cell(style["left_column"], 9, resume_config["blurb"], align="L")
    pdf.ln()


def _section_header(title, pdf, style):
    pdf.ln()
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(31, 121, 199)
    pdf.cell(125, 9, title.upper())


def _add_experience(resume_config, pdf, style):
    _section_header("Experience", pdf, style)
    y = pdf.get_y()
    pdf.set_text_color(0, 0, 0)
    y = y + 9
    pdf.set_y(y)
    for experience in resume_config["experience"][0:3]:
        pdf.set_text_color(0, 0, 0)
        y = pdf.get_y()
        pdf.set_font("Helvetica", "B", 12)
        cell_width = pdf.get_string_width(experience["company"])
        pdf.cell(cell_width, 12, experience["company"])
        pdf.set_font("Helvetica", "", 12)
        location = f", {experience['location']} - "
        cell_width = pdf.get_string_width(location)
        pdf.cell(cell_width, 12, location)
        pdf.set_font("Helvetica", "I", 12)
        cell_width = pdf.get_string_width(experience["title"])
        pdf.cell(cell_width, 12, experience["title"])
        y = y + 7
        pdf.set_y(y)
        pdf.set_text_color(100, 100, 100)
        pdf.set_font("Helvetica", "", 9)
        pdf.cell(125, 9, experience["dates"])
        y = y + 9
        pdf.set_y(y)
        pdf.multi_cell(125, 5, experience["description"])


def _add_additional_experience(resume_config, pdf, style):
    _section_header("Additional Work Experience", pdf, style)
    pdf.ln()
    for experience in resume_config["experience"][3:]:
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Helvetica", "B", 9)
        cell_width = pdf.get_string_width(experience["company"])
        pdf.cell(cell_width, 5, experience["company"])
        pdf.set_text_color(100, 100, 100)
        pdf.set_font("Helvetica", "", 9)
        right = f" - {experience['location']} - {experience['title']} - {experience['dates']}"
        cell_width = pdf.get_string_width(right)
        pdf.cell(cell_width, 5, right)
        pdf.ln()


def _add_education(resume_config, pdf, style):
    _section_header("Education", pdf, style)
    pdf.ln()
    for education in resume_config["education"]:
        pdf.set_text_color(0, 0, 0)
        y = pdf.get_y()
        pdf.set_font("Helvetica", "B", 12)
        cell_width = pdf.get_string_width(education["school"])
        pdf.cell(cell_width, 12, education["school"])
        pdf.set_font("Helvetica", "", 12)
        location = f", {education['location']} - "
        cell_width = pdf.get_string_width(location)
        pdf.cell(cell_width, 12, location)
        pdf.set_font("Helvetica", "I", 12)
        cell_width = pdf.get_string_width(education["degree"])
        pdf.cell(cell_width, 12, education["degree"])
        y = y + 7
        pdf.set_y(y)
        pdf.set_text_color(100, 100, 100)
        pdf.set_font("Helvetica", "", 9)
        pdf.cell(125, 9, education["dates"])
        pdf.ln()


def _text_cell(value, pdf, height):
    pdf.cell(pdf.get_string_width(value), height, value)


def _add_contact(resume_config, pdf, style):
    pdf.set_text_color(0, 0, 0)
    pdf.set_left_margin(150)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_y(15)
    _text_cell(resume_config["phone"], pdf, 5)
    pdf.ln()
    _text_cell(resume_config["email"], pdf, 5)
    pdf.ln()
    _text_cell(resume_config["website"], pdf, 5)


def _add_skills(resume_config, pdf, style):
    pdf.set_y(45)
    _section_header("Skills", pdf, style)
    pdf.ln()
    pdf.set_text_color(100, 100, 100)
    pdf.set_font("Helvetica", "", 9)

    for skill in resume_config["skills"]:
        _text_cell(skill, pdf, 9)
        pdf.ln()


def _add_projects(resume_config, pdf, style):
    _section_header("Projects", pdf, style)
    pdf.ln()
    for project in resume_config["projects"]:
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(0, 0, 0)
        _text_cell(project["name"], pdf, 10)
        pdf.ln()
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(100, 100, 100)
        pdf.multi_cell(50, 5, project["description"], align="L")
        pdf.ln()


def convert_resume():
    pdf = FPDF(format="letter")
    style = {"left_column": 125, "headline_font_size": 36}
    with open("resume.yml", "r") as resume_file:
        resume_config = yaml.safe_load(resume_file)
        pdf.add_page()
        _add_header(resume_config, pdf, style)
        _add_experience(resume_config, pdf, style)
        _add_additional_experience(resume_config, pdf, style)
        _add_education(resume_config, pdf, style)
        _add_contact(resume_config, pdf, style)
        _add_skills(resume_config, pdf, style)
        _add_projects(resume_config, pdf, style)
    pdf.output("resume.pdf", "F")


if __name__ == "__main__":
    convert_resume()
