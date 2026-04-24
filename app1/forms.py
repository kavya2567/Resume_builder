from django import forms

class ResumeForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=15)
    linkedin = forms.URLField(required=False)
    github = forms.URLField(required=False)

    career_objective = forms.CharField(widget=forms.Textarea)

    skills = forms.CharField(widget=forms.Textarea)
    education = forms.CharField(widget=forms.Textarea)
    experience = forms.CharField(widget=forms.Textarea)
    projects = forms.CharField(widget=forms.Textarea)

    certifications = forms.CharField(widget=forms.Textarea, required=False)
    hobbies = forms.CharField(widget=forms.Textarea, required=False)