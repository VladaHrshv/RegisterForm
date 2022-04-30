from flask import Flask, render_template, request

from data import db_session
from forms.regin_form import RegisterForm
from data.users import User
from data.jobs import Jobs

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('regin.html', title='Форма регистрации',
                                   form=form,
                                   message="Пароли не совпадают")

        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.login.data).first():
            return render_template('regin.html', title='Форма Регистрации',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            email=form.login.data,
            hashed_password=form.password.data
        )
        db_sess.add(user)
        db_sess.commit()

    return render_template('regin.html', title='Форма регистрации', form=form)


def main():
    db_session.global_init(f"db/mars.db")
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()