from django.shortcuts import render
from django.http import HttpResponse
from app1.forms import ResumeForm

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def wrap_text(text, max_chars=100):
    lines = []
    words = text.split()
    current_line = ""

    for word in words:
        if len(current_line + word) < max_chars:
            current_line += word + " "
        else:
            lines.append(current_line)
            current_line = word + " "

    if current_line:
        lines.append(current_line)

    return lines


def resume_view(request):
    if request.method == "POST":
        form = ResumeForm(request.POST)

        if form.is_valid():
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="resume.pdf"'

            # ✅ Load Calibri fonts
            pdfmetrics.registerFont(TTFont('Calibri', 'C:/Windows/Fonts/calibri.ttf'))
            pdfmetrics.registerFont(TTFont('Calibri-Bold', 'C:/Windows/Fonts/calibrib.ttf'))

            p = canvas.Canvas(response, pagesize=A4)
            data = form.cleaned_data

            y = 800

            # ✅ Name (slightly bigger)
            p.setFont("Calibri-Bold", 14)
            p.drawString(200, y, data['name'])

            y -= 25

            # ✅ Content font (Calibri 10)
            p.setFont("Calibri", 10)

            # Contact Info
            p.drawString(50, y, f"Email: {data['email']}")
            y -= 12

            p.drawString(50, y, f"Phone: {data['phone']}")
            y -= 12

            if data.get('linkedin'):
                p.drawString(50, y, f"LinkedIn: {data['linkedin']}")
                y -= 12

            if data.get('github'):
                p.drawString(50, y, f"GitHub: {data['github']}")
                y -= 12

            y -= 15

            # ✅ Section function
            def section(title, content):
                nonlocal y

                if not content:
                    return

                # 🔹 Heading → Calibri Bold 11
                p.setFont("Calibri-Bold", 11)
                p.drawString(50, y, title)
                y -= 15

                # 🔹 Content → Calibri 10
                p.setFont("Calibri", 10)

                lines = content.split("\n")

                for line in lines:
                    wrapped_lines = wrap_text(line)

                    for wrap_line in wrapped_lines:
                        if y < 50:
                            p.showPage()
                            p.setFont("Calibri", 10)
                            y = 800

                        p.drawString(60, y, wrap_line)
                        y -= 12

                y -= 8

            # Sections
            section("Career Objective", data.get('career_objective', ''))
            section("Skills", data.get('skills', ''))
            section("Education", data.get('education', ''))
            section("Experience", data.get('experience', ''))
            section("Projects", data.get('projects', ''))
            section("Certifications", data.get('certifications', ''))
            section("Hobbies", data.get('hobbies', ''))

            p.save()
            return response

    else:
        form = ResumeForm()

    return render(request, "home.html", {"form": form})