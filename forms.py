from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, IntegerField, PasswordField, SelectField, BooleanField, FileField
from wtforms.validators import DataRequired, Length, NumberRange, Email, EqualTo, Optional, ValidationError
from flask_wtf.file import FileAllowed
from app.models.user import User

class ReviewForm(FlaskForm):
    rating = IntegerField('Rating', validators=[DataRequired(), NumberRange(min=1, max=5)])
    comment = TextAreaField('Comment', validators=[DataRequired(), Length(min=1, max=500)])
    submit = SubmitField('Submit Review')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class AdvancedSearchForm(FlaskForm):
    query = StringField('Search', validators=[Optional()])
    category = SelectField('Category', 
                         coerce=lambda x: int(x) if x else None,
                         validators=[Optional()],
                         choices=[('', 'All')])
    location = StringField('Location', validators=[Optional()])
    target_audience = SelectField('Target Audience', 
                                choices=[('', 'All'), ('men', 'Men'), ('women', 'Women'), ('kids', 'Kids')],
                                validators=[Optional()])
    price_range = SelectField('Price Range',
                            choices=[('', 'All'), ('low', 'Low'), ('medium', 'Medium'), ('high', 'High')],
                            validators=[Optional()])
    submit = SubmitField('Search')

    def __init__(self, *args, **kwargs):
        super(AdvancedSearchForm, self).__init__(*args, **kwargs)
        from app.models import Category
        categories = Category.query.all()
        self.category.choices = [('', 'All')] + [(str(c.id), c.name) for c in categories]

class ProfileForm(FlaskForm):
    username = StringField('Nom d\'utilisateur', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('Prénom', validators=[Optional(), Length(max=64)])
    last_name = StringField('Nom', validators=[Optional(), Length(max=64)])
    bio = TextAreaField('Biographie', validators=[Optional(), Length(max=500)])
    location = StringField('Localisation', validators=[Optional(), Length(max=100)])
    phone_number = StringField('Numéro de téléphone', validators=[Optional(), Length(max=20)])
    profile_picture = FileField('Photo de profil')
    submit = SubmitField('Mettre à jour')

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Mot de passe actuel', validators=[DataRequired()])
    new_password = PasswordField('Nouveau mot de passe', validators=[
        DataRequired(),
        Length(min=8, message='Le mot de passe doit contenir au moins 8 caractères')
    ])
    confirm_password = PasswordField('Confirmer le mot de passe', validators=[
        DataRequired(),
        EqualTo('new_password', message='Les mots de passe doivent correspondre')
    ])
    submit = SubmitField('Changer le mot de passe')

class PostForm(FlaskForm):
    title = StringField('Titre', validators=[DataRequired(), Length(max=200)])
    content = TextAreaField('Contenu', validators=[DataRequired()])
    image = FileField('Image')
    submit = SubmitField('Publier')

class BoutiqueForm(FlaskForm):
    name = StringField('Nom', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Description', validators=[DataRequired()])
    address = StringField('Adresse', validators=[DataRequired()])
    category_id = SelectField('Catégorie', coerce=int, validators=[DataRequired()])
    target_audience = SelectField('Public cible', 
                                choices=[('all', 'Tous'), ('men', 'Hommes'), ('women', 'Femmes'), ('kids', 'Enfants')],
                                validators=[DataRequired()])
    submit = SubmitField('Enregistrer')

class EditProfileForm(FlaskForm):
    username = StringField('Nom d\'utilisateur', 
                          validators=[DataRequired(), 
                                    Length(min=3, max=64)])
    first_name = StringField('Prénom', 
                           validators=[Optional(), 
                                     Length(max=64)])
    last_name = StringField('Nom', 
                          validators=[Optional(), 
                                    Length(max=64)])
    email = StringField('Email', 
                       validators=[DataRequired(), 
                                 Email(), 
                                 Length(max=120)])
    location = StringField('Localisation', 
                          validators=[Optional(), 
                                    Length(max=128)])
    bio = TextAreaField('Biographie', 
                       validators=[Optional(), 
                                 Length(max=500)])
    profile_picture = FileField('Photo de profil', 
                              validators=[Optional(),
                                        FileAllowed(['jpg', 'jpeg', 'png'], 
                                                  'Images uniquement!')])
    submit = SubmitField('Enregistrer les modifications')

    def __init__(self, original_username, original_email, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=username.data).first()
            if user is not None:
                raise ValidationError('Ce nom d\'utilisateur est déjà pris. Veuillez en choisir un autre.')

    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=email.data).first()
            if user is not None:
                raise ValidationError('Cet email est déjà utilisé. Veuillez en utiliser un autre.')