from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, ClientForm, ShootForm
from flask_login import current_user, login_user, login_required
from app.models import User, Client, MailingAddress, Shoot
from flask_login import logout_user
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/clientform', methods=['GET','POST'])
def clientform():
    form = ClientForm()
    if form.validate_on_submit():
        client = Client(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data, phone=form.phone.data, payment_information=form.payment_information.data)
        mailing_address = MailingAddress(street=form.street.data, city=form.city.data, state=form.state.data, postal_code=form.postal_code.data, country=form.country.data, client_id=client.id)
        db.session.add(client)
        db.session.add(mailing_address)
        db.session.commit()
        flash('Client Information Entered Successfully')
        return redirect(url_for('index'))
    return render_template('clientform.html', title='Client Information', form=form)

@app.route('/shootform', methods=['GET', 'POST'])
def shootform():
    form = ShootForm()
    if form.validate_on_submit():
        shoot = Shoot(locations=form.locations.data, client_id=form.client_id.data, time=form.time.data,prompt=form.prompt.data, equipment=form.equipment.data, num_photos_requested=form.num_photos_requested.data, model_release=form.model_release.data, branding=form.branding.data)
        db.session.add(shoot)
        db.session.commit()
        flash('Shoot information saved successfully.')
        return redirect(url_for('index'))
    return render_template('shootform.html', title='Shoot Information Form', form=form)

@app.route('/clientinfo', methods=['GET', 'POST'])
def clientinfo():
    form = ShootForm()
    form.client_id.choices = [(c.id, f"{c.first_name} {c.last_name}") for c in Client.query.order_by(Client.first_name)]
    selected_client = None

    if request.method == 'POST':
        client_id = form.client_id.data
        selected_client = Client.query.get(client_id)

    return render_template('clientinfo.html', form=form, selected_client=selected_client)

@app.route('/shootinfo', methods=['GET', 'POST'])
def shootinfo():
    form = ShootForm()
    form.client_id.choices = [(c.id, f"{c.first_name} {c.last_name}") for c in Client.query.order_by(Client.first_name)]
    shoots = None

    if request.method == 'POST':
        client_id = form.client_id.data
        shoots = Shoot.query.filter_by(client_id=client_id).all()

    return render_template('shootinfo.html', form=form, shoots=shoots)