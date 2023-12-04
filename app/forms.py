from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DecimalField, TextAreaField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, NumberRange, Email, EqualTo
from wtforms import validators

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('password')])
    phone = StringField('Telefone', validators=[DataRequired(), Length(min=8, max=15)])
    address = StringField('Endereço', validators=[DataRequired(), Length(min=5, max=100)])
    submit = SubmitField('Registrar')


class UpdateProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Telefone', validators=[DataRequired(), Length(min=8, max=15)])
    address = StringField('Endereço', validators=[DataRequired(), Length(min=5, max=100)])
    submit = SubmitField('Salvar')


class ProductForm(FlaskForm):
    name = StringField('Nome', validators=[DataRequired(), Length(max=100)])
    quantity = IntegerField('Quantidade em estoque', validators=[DataRequired(), NumberRange(min=0)])
    price = DecimalField('Preço', validators=[DataRequired(), NumberRange(min=0)])
    description = TextAreaField('Descrição', validators=[DataRequired(), Length(max=500)])
    ingredients = TextAreaField('Ingredientes', validators=[DataRequired()])
    submit = SubmitField('Adicionar Produto')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[validators.InputRequired(), validators.Email()])
    password = PasswordField('Senha', validators=[validators.InputRequired()])
    submit = SubmitField('Login')