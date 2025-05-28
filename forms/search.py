from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField


class AdvancedSearchForm(FlaskForm):
    target_audience = SelectField('Public cible', choices=[
        ('', 'Tous'),
        ('homme', 'Homme'),
        ('femme', 'Femme'),
        ('ado', 'Adolescent'),
        ('enfant', 'Enfant')
    ])
    
    price_range = SelectField('Gamme de prix', choices=[
        ('', 'Tous'),
        ('eco', 'Économique'),
        ('moyen', 'Moyen'),
        ('premium', 'Premium'),
        ('luxe', 'Luxe')
    ])
    
    category = SelectField('Catégorie', choices=[])  # Rempli dynamiquement
    location = StringField('Quartier')
    submit = SubmitField('Rechercher')