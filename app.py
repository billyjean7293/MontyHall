from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'secret, create your own'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/monty_hall', methods=['GET', 'POST'])
def monty_hall():
    if request.method == 'POST':
        user_choice = int(request.form['door'])
        doors = [0, 1, 2]
        car = random.choice(doors)
        doors.remove(user_choice)
        if user_choice == car:
            goat = random.choice(doors)
        else:
            goat = car if user_choice in doors else random.choice(doors)
        session['car'] = car
        session['user_choice'] = user_choice
        session['goat'] = goat
        return redirect(url_for('monty_hall_reveal'))
    return render_template('monty_hall.html')


@app.route('/monty_hall_reveal', methods=['GET', 'POST'])
def monty_hall_reveal():
    car = session.get('car')
    user_choice = session.get('user_choice')
    goat = session.get('goat')
    remaining_door = 3 - user_choice - goat

    if request.method == 'POST':
        switch = request.form['switch']
        final_choice = remaining_door if switch == 'yes' else user_choice
        result = 'won' if final_choice == car else 'lost'
        return render_template('monty_hall_result.html', result=result,
                               car=car)

    return render_template('monty_hall_reveal.html', goat=goat,
                           remaining_door=remaining_door)


if __name__ == '__main__':
    app.run(debug=True)
