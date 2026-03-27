# auth/forms.py
from datetime import date
from flask import current_app
from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, BooleanField, SubmitField
)
from wtforms.fields import DateField
from wtforms.validators import (
    DataRequired, Email, Length, EqualTo, Regexp, ValidationError, optional
)

# --- Form definitions + validators ---
# Allow letters, spaces, hyphens, apostrophes; 2–120 chars total
NAME_PATTERN = r"^[A-Za-z][A-Za-z\s\-’']{1,119}$"

def valid_name(form, field):
    text = (field.data or "").strip()
    if not text:
        raise ValidationError("Name is required.")
def strong_password(form, field):
    pw = field.data or ""
    if len(pw) < 10:
        raise ValidationError("Password must be at least 10 characters long.")
    if not any(c.isdigit() for c in pw):
        raise ValidationError("Password must include at least one number.")
    if not any(not c.isalnum() for c in pw):
        raise ValidationError("Password must include at least one symbol.")
    if not any(c.isupper() for c in pw):
        raise ValidationError("Password must include at least one uppercase letter.")

def normalize_name(name: str) -> str:
    return " ".join(part.capitalize() for part in (name or "").split())


def validate_staff_code(self, field):
        expected = current_app.config.get("ADMIN_CODE") or current_app.config.get("PRODUCER_CODE")
        if field.data != expected:
            raise ValidationError("Invalid staff code.")

def validate_dob(form, field):
    dob = field.data
    today = date.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    if age < 13:
        raise ValidationError("You must be at least 13 years old to register.")


# --- Forms ---
class RegisterForm(FlaskForm):
    full_name = StringField(
        "Full name",
        render_kw={"placeholder": "Full name"},
        validators=[
            DataRequired(),
            Length(min=2, max=120),
            Regexp(NAME_PATTERN, message="Use letters, spaces, hyphens or apostrophes."),
        ],
    )
    email = StringField("Email", render_kw={"placeholder": "Email"}, validators=[DataRequired(), Email()])
    
    phone_number = StringField(
        'Phone Number',
        render_kw={"placeholder": "Phone Number"},
        validators=
        [DataRequired(),
        Regexp(r'^\+?\d{10,15}$', message="Enter a valid phone number.")
    ])
    password = PasswordField(
        "Password",
        render_kw={"placeholder": "Password"},
        validators=[DataRequired(), Length(min=10), strong_password],
    )
    confirm = PasswordField(
        "Confirm password",
        render_kw={"placeholder": "Confirm Password"},
        validators=[DataRequired(), EqualTo("password", message="Passwords must match.")],
    )
    # HTML date inputs send YYYY-MM-DD; DateField parses to a date object.
    dob = DateField("Date of birth", render_kw={"placeholder": "dd / mm / yyyy", "type": "date"}, format="%Y-%m-%d", validators=[DataRequired(), validate_dob])

    staff_code = StringField(
        "Staff Code",
        render_kw={"placeholder": "Staff Code"},
        validators=[optional()] + [validate_staff_code]
    )

    submit = SubmitField("Begin My Journey")


class LoginForm(FlaskForm):
    email = StringField("Email", render_kw={"placeholder": "Email"}, validators=[DataRequired(), Email()])
    password = PasswordField("Password", render_kw={"placeholder": "Password"}, validators=[DataRequired()])
    remember = BooleanField("Remember me")
    submit = SubmitField("Continue My Journey")


class ProfileForm(FlaskForm):
    full_name = StringField(
        "Full name",
        validators=[
            valid_name,
            Length(min=2, max=49),
            Regexp(NAME_PATTERN, message="Use letters, spaces, hyphens or apostrophes."),
        ],
    )
    email = StringField(
        "Email",
        validators=[DataRequired(), Email()],
    )
    phone_number = StringField('Phone Number', [
        DataRequired(),
        Regexp(r'^\+?\d{10,15}$', message="Enter a valid phone number.")
    ])
    submit = SubmitField("Save changes")


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField("Current password", validators=[DataRequired()])
    new_password = PasswordField(
        "New password",
        validators=[DataRequired(), strong_password],
    )
    confirm = PasswordField(
        "Confirm new password",
        validators=[DataRequired(), EqualTo("new_password", message="Passwords must match.")],
    )
    submit = SubmitField("Update password")

class DeleteAccountForm(FlaskForm):
    password = PasswordField("Confirm password", validators=[DataRequired()])
    confirm = BooleanField(
        "I understand this will permanently delete my account",
        validators=[DataRequired()],
    )
    delete_submit = SubmitField("Delete account")