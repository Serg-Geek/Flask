# Создать страницу, на которой будет форма для ввода имени и электронной почты, при отправке которой будет 
# создан cookie-файл с данными пользователя, а также будет произведено перенаправление на страницу приветствия,
# где будет отображаться имя пользователя.
# На странице приветствия должна быть кнопка «Выйти», при нажатии на которую будет удалён cookie-файл с данными 
# пользователя и произведено перенаправление на страницу ввода имени и электронной почты.

from flask import Flask, render_template, request, redirect, make_response

app = Flask(__name__)

# Маршрут для отображения страницы с формой ввода данных пользователя
@app.route("/")
def index():
    return render_template("index.html")

# Маршрут для обработки отправки формы и отображения страницы приветствия
@app.route("/welcome", methods=["GET", "POST"])
def welcome():
    # При отправке данных из формы на метод POST
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        response = make_response(redirect("/welcome"))
        response.set_cookie("user", name, max_age=60*60*24*365)  # Сохраняем имя пользователя в куке на 1 год
        return response
    # При первом открытии страницы приветствия методом GET
    else:
        user = request.cookies.get("user")
        if user:
            return render_template("welcome.html", user=user)
        else:
            return redirect("/")

# Маршрут для выхода из аккаунта и удаления куки пользователя
@app.route("/logout")
def logout():
    response = make_response(redirect("/"))
    response.set_cookie("user", "", expires=0)  # Удаляем куку пользователя
    return response

if __name__ == "__main__":
    app.run(debug=True)
