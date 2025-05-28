from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, Length, Optional, EqualTo


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