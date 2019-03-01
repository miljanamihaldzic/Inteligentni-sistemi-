from wtforms import Form, BooleanField, StringField, TextAreaField, PasswordField,validators,SubmitField,SelectField,IntegerField
from flask_wtf.file import FileField, FileAllowed
from flask_wtf import FlaskForm
from wtforms.fields.html5 import DecimalRangeField

class MainForm(FlaskForm):
  
    picture = FileField('Choose picture', validators = [FileAllowed(['jpg','png'])])

    shape = SelectField('Shape',choices=[(8,'Circle'),(3,'Triangle'),(6,'Hexagon'),(4,'Rectanfle')])

    color = SelectField('Color',choices=[('R','Red'),('G','Green'),('B','Blue')])
    
    surface = IntegerField('Surface in px ',[validators.NumberRange(min =1)],default= 3000)
    
    brightness = DecimalRangeField('Brightness', [validators.NumberRange(min =1, max = 100)],default=50)

    contrast = DecimalRangeField('Contrast',[validators.NumberRange(min =1, max = 100)],default=50)

    edge = BooleanField('Display edges')

    submit = SubmitField('Save')
    