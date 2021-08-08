from flask import Flask, render_template, url_for, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TimeField, SelectField
from wtforms.validators import DataRequired, URL
import csv


app = Flask(__name__)
app.config['SECRET_KEY'] = "blablabla"
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField(label='Cafe name', validators=[DataRequired()])
    location = StringField(label="Lacation URL", validators=[DataRequired(), URL()])
    open_time = TimeField(label="Open time e.g. 8AM", validators=[DataRequired()])
    closing_time = TimeField(label="Closing time in 2 format e.g 15:30", validators=[DataRequired()])
    coffee_rating = SelectField(label="Coffee raiting", choices=["☕", "☕☕", "☕☕☕", "☕☕☕☕", "☕☕☕☕☕"],
                                validators=[DataRequired()])
    wifi_rating = SelectField(label="Wifi strength", choices=["✘", "💪", "💪💪", "💪💪💪", "💪💪💪💪", "💪💪💪💪💪"],
                              validators=[DataRequired()])
    power_outlet = SelectField(label="Power sockets availability",
                               choices=["✘", "🔌", "🔌🔌", "🔌🔌🔌", "🔌🔌🔌🔌", "🔌🔌🔌🔌🔌"],
                               validators=[DataRequired()])
    submit = SubmitField(label='Submit')



@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["POST", "GET"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        with open('cafe-data.csv', mode="a", encoding="utf8") as csv_file:
            csv_file.write(
                f"\n{form.cafe.data},{form.location.data},{form.open_time.data.strftime('%I:%M %p')},{form.closing_time.data.strftime('%I:%M %p')},{form.coffee_rating.data},{form.wifi_rating.data},{form.power_outlet.data}")
        return redirect(url_for('cafes'))


    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding="utf8") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)






if __name__ == '__main__':
    app.run(debug=True)
