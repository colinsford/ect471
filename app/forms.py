from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User, Client, MailingAddress, Shoot

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
        
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
        
class ClientForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    phone = StringField('Phone')
    payment_information = StringField('Payment Information')
    street = StringField('Street')
    city = StringField('City')
    state = StringField('State')
    postal_code = StringField('Postal Code')
    country = StringField('Country')
    submit = SubmitField('Submit')

class ShootForm(FlaskForm):
    locations = StringField('Location')
    client_id = SelectField(u'Client', coerce=int)
    time = StringField('Time/Date')
    prompt = StringField('Shoot Prompt')
    equipment = StringField('Equipment')
    num_photos_requested = IntegerField('Number of Photos Requested')
    model_release = StringField('Model Release?')
    branding = StringField('Link to Branding / Graphics')
    
    def edit_client(request, id):
        client = Client.query.get(id)
        form = ShootForm(request.POST, obj=client)
        form.client_id.choices = [(c.id, c.first_name, c.last_name) for c in Client.query.order_by('name')]

