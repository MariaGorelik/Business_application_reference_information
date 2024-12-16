from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from orm_models import db, Artist, Song, Dictionary, DictionaryFields

app = Flask(__name__)

# Database URI
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pymssql://sa:486319@LAPTOP-1M8OJBHN\\SQLEXPRESS/Music_information'
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc://sa:486319@LAPTOP-1M8OJBHN\\SQLEXPRESS/Music_information?driver=ODBC+Driver+17+for+SQL+Server"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Fixed syntax

# Initialize the SQLAlchemy object
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/<dictionary>', methods=['GET'])
def get_dictionary(dictionary):
    # Извлекаем справочник по имени
    dictionary_entry = Dictionary.query.filter_by(name=dictionary).first()

    if not dictionary_entry:
        return "Invalid dictionary", 404

    # Извлекаем все поля для этого справочника
    dictionary_fields = DictionaryFields.query.filter_by(dictionaryId=dictionary_entry.id).all()

    if not dictionary_fields:
        return "No fields found for this dictionary", 404

    # Составляем список полей для отображения
    fields = [field.fieldName for field in dictionary_fields]

    # Динамическое получение модели таблицы
    model_class = globals().get(dictionary_entry.name)

    if not model_class:
        return "Model not found", 404

    # Получаем все записи из соответствующей таблицы
    data = model_class.query.all()

    # Передаем данные в шаблон
    return render_template('table.html', data=data, fields=fields, getattr=getattr)


@app.route('/api/<dictionary>', methods=['POST'])
def add_entry(dictionary):
    # Извлекаем справочник по имени
    dictionary_entry = Dictionary.query.filter_by(name=dictionary).first()

    if not dictionary_entry:
        return "Invalid dictionary", 404

    # Извлекаем все поля для этого справочника
    dictionary_fields = DictionaryFields.query.filter_by(dictionaryId=dictionary_entry.id).all()

    # Динамическое получение модели таблицы
    model_class = globals().get(dictionary_entry.name)

    if not model_class:
        return "Model not found", 404

    # Создаем новый объект модели с данными из формы
    field_values = {}

    for field in dictionary_fields:
        field_values[field.fieldName] = request.form.get(field.fieldName)

    # Создаем экземпляр модели с переданными значениями
    entry = model_class(**field_values)

    # Добавляем запись в базу данных
    db.session.add(entry)
    db.session.commit()

    # Перенаправляем на страницу с данными справочника
    return redirect(url_for('get_dictionary', dictionary=dictionary))


@app.route('/api/dictionaries', methods=['GET'])
def get_dictionaries():
    # Извлекаем все записи из таблицы Dictionary
    dictionaries = Dictionary.query.all()
    # Преобразуем их в формат JSON
    return [{"name": dictionary.name, "displayName": dictionary.displayName} for dictionary in dictionaries]


if __name__ == '__main__':
    app.run(debug=True)
