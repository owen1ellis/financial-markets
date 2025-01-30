from flask import Flask, render_template, request
from website import create_app
import pandas as pd
from loguru import logger

from data_fetcher import EarningsData, IncomeData

app = Flask(__name__, template_folder='website/templates')

earnings = EarningsData()
income = IncomeData()

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    user_input = ""
    earnings_df = pd.DataFrame({})
    income_df = pd.DataFrame({})
    table_html = pd.DataFrame({})
    if request.method == "POST":
        user_input = request.form.get("text_input")  # Get input from form
        if user_input is not None:
            earnings_df = earnings.get_eps(user_input)
            income_df = income.get_data(user_input)

    table_html = earnings_df.to_html(classes="table table-striped", index=False)  # Convert DataFrame to HTML
    income_tbl_html = income_df.to_html(classes="table table-striped", index=False)  # Convert DataFrame to HTML
    return render_template("index.html", table=table_html, user_input=user_input, income_table=income_tbl_html)

    

if __name__ == '__main__':
    app.run(debug=True)