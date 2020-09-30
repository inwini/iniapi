
from . import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):

	__tablename__ = 'users'
	id = db.Column(
		db.Integer,
		primary_key=True
	)
	username = db.Column(
		db.String(100),
		nullable=False,
		unique=True
	)
	email = db.Column(
		db.String(40),
		unique=False,
		nullable=False
	)
	password = db.Column(
		db.String(200),
		primary_key=False,
		unique=False,
		nullable=False
	)
	image = db.Column(
		db.String(250),
		primary_key=False,
		unique=False,
		nullable=False
	)
	role_id = db.Column(
		db.Integer,
		index=False,
		unique=False,
		nullable=True
	)
	status = db.Column(
		db.Integer,
		index=False,
		unique=False,
		nullable=True
	)
	created_at = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        default=db.func.current_timestamp()
    )
	updated_at = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        default=db.func.current_timestamp(),
		onupdate=db.func.current_timestamp()
    )

	def set_password(self, password):

		self.password = generate_password_hash(password, method='sha256')

	def check_password(self, password):

		return check_password_hash(self.password, password)

	def __repr__(self):

		return f"<id={self.id}, username={self.username}, email={self.email}, image={self.image}, role_id={self.role_id}, status={self.status}, created_at={self.created_at}, updated_at={self.updated_at}>"

class Build(db.Model):

	__tablename__ = 'builds'
	id = db.Column(
		db.Integer,
		primary_key=True
	)
	user_id = db.Column(
		db.Integer,
		index=False,
		unique=True,
		nullable=True
	)
	build_name = db.Column(
		db.String(100),
		nullable=False,
		unique=False,
	)
	build_image = db.Column(
		db.String(250),
		nullable=False,
		unique=False,
	)
	
	created_at = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        default=db.func.current_timestamp()
    )
	updated_at = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        default=db.func.current_timestamp(),
		onupdate=db.func.current_timestamp()
    )

	def __repr__(self):
		return f"<id={self.id},user_id={self.user_id},build_name={self.build_name},created_at={self.created_at},updated_at={self.updated_at}>"

class Department(db.Model):

	__tablename__ = 'departments'
	id = db.Column(
		db.Integer,
		primary_key=True
	)
	department_name = db.Column(
		db.String(100),
		nullable=False,
		unique=False
	)
	build_id = db.Column(
		db.Integer,
		index=False,
		unique=False,
		nullable=True
	)
	created_at = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        default=db.func.current_timestamp()
    )
	updated_at = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        default=db.func.current_timestamp(),
		onupdate=db.func.current_timestamp()
    )
	def __repr__(self):
		return f"<id={self.id}, department_name={self.department_name}, build_id={self.build_id}, created_at={self.created_at}, updated_at={self.updated_at}>"

class Build_Log(db.Model):

	__tablename__ = 'build_logs'
	id = db.Column(
		db.Integer,
		primary_key=True
	)
	build_id = db.Column(
		db.Integer,
		index=False,
		unique=False,
		nullable=True
	)
	license_plate = db.Column(
		db.String(100),
		nullable=False,
		unique=False
	)
	department_id = db.Column(
		db.Integer,
		index=False,
		unique=False,
		nullable=True
	)
	variable_a = db.Column(
		db.Float,
		index=False,
		unique=False,
		nullable=True
	)
	variable_b = db.Column(
		db.Float,
		index=False,
		unique=False,
		nullable=True
	)
	variable_c = db.Column(
		db.Float,
		index=False,
		unique=False,
		nullable=True
	)
	created_at = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        default=db.func.current_timestamp()
    )
	updated_at = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        default=db.func.current_timestamp(),
		onupdate=db.func.current_timestamp()
    )
	def __repr__(self):
		return f"<id={self.id}, build_id={self.build_id}, license_plate={self.license_plate}, department_id={self.department_id}, variable_a={self.variable_a}, variable_b={self.variable_b}, variable_c={self.variable_c}, created_at={self.created_at}, updated_at={self.updated_at}>"
