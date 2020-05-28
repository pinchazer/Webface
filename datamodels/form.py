from wtforms import Form, StringField, TextAreaField, validators

#valid = [validators.DataRequired(), validators.Regexp('[0-9.]+', message='Only numbers')]
valid_iris = [validators.Regexp('[0-9.]+', message='Only numbers')]
valid_text = [validators.DataRequired(), validators.length(max=200, message='200 symbols allowed')]
class IrisForm(Form):
    sl = StringField('sepal_len', validators=valid_iris, render_kw={'placeholder': "Sepal Length", 'class': 'form-control'})
    sw = StringField('sepal_wid', validators=valid_iris, render_kw={'placeholder': "Sepal Width", 'class': 'form-control'})
    pl = StringField('petal_len', validators=valid_iris, render_kw={'placeholder': "Petal Length", 'class': 'form-control'})
    pw = StringField('petal_wid', validators=valid_iris, render_kw={'placeholder': "Petal Width", 'class': 'form-control'})

class TextForm(Form):
    txtfld = TextAreaField('TextArea',validators=valid_text, render_kw={'class': 'form-control'})
