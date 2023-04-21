from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Optional
from wtforms_sqlalchemy.fields import QuerySelectField
from app.models import User, Client, MailingAddress, Shoot, Camera, Lens

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

def available_cameras():
    return Camera.query.all()

class ShootForm(FlaskForm):
    locations = StringField('Location')
    client_id = SelectField(u'Client', coerce=int)
    time = StringField('Time/Date')
    prompt = StringField('Shoot Prompt')
    camera = QuerySelectField('Camera', query_factory=available_cameras, get_label='model', allow_blank=True, id='camera-select')
    lens = QuerySelectField('Lens', query_factory=lambda: [], get_label='model', allow_blank=True, id='lens-select', validators=[Optional()])
    num_photos_requested = IntegerField('Number of Photos Requested')
    model_release = StringField('Model Release?')
    branding = StringField('Link to Branding / Graphics')
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(ShootForm, self).__init__(*args, **kwargs)
        self.client_id.choices = [(c.id, f'{c.first_name} {c.last_name}') for c in Client.query.order_by(Client.last_name, Client.first_name)]

    def validate_client_id(self, client_id):
        client = Client.query.get(client_id.data)
        if client is None:
            raise ValidationError('Not a valid choice.')
        
    def validate(self):
        # Remove validation for the lens field
        del self.lens.validators[:]
        # Run the default validation process
        return super(ShootForm, self).validate()

def available_cameras():
    return Camera.query.all()

class CameraForm(FlaskForm):
    brand = StringField('Brand')
    model = StringField('Model')
    submit = SubmitField('Submit')

class LensForm(FlaskForm):
    brand = StringField('Brand')
    model = StringField('Model')
    camera = QuerySelectField('Camera', query_factory=available_cameras, get_label='model', allow_blank=True)
    submit = SubmitField('Submit')

def edit_client(request, id):
    client = Client.query.get(id)
    form = ShootForm(request.POST, obj=client)
    form.client_id.choices = [(c.id, f'{c.first_name} {c.last_name}') for c in Client.query.order_by(Client.last_name, Client.first_name)]

