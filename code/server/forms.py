# forms.py

from wtforms import Form, StringField


class SearchForm(Form):
    """
    Form for generating a search bar in the homepage
    """
    search = StringField('')
