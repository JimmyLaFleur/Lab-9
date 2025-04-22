from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask('Портфолио')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Repositories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300))
    link = db.Column(db.String(500))

@app.route("/")
def main():
    repositories = Repositories.query.all()
    return render_template('index.html', products_list=repositories)

@app.route('/add_repositories', methods=['POST'])
def add_repositories():
    # Получаем данные из формы
    title = request.form.get('title')
    link = request.form.get('link')

    if title and link:
        # Создаем новый объект репозитория и сохраняем в базе данных
        new_repository = Repositories(title=title, link=link)
        db.session.add(new_repository)
        db.session.commit()
        return 'Репозиторий добавлен!'
    return 'Ошибка при добавлении репозитория.'

@app.route('/clear_repositories', methods=['POST'])
def clear_repositories():
    try:
        num_rows_deleted = db.session.query(Repositories).delete()
        db.session.commit()
        return f'{num_rows_deleted} записей удалено.'
    except Exception as e:
        db.session.rollback()
        return f'Ошибка: {str(e)}', 500



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
