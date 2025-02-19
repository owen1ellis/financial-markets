from flask import Flask, render_template, request
from website import create_app
import pandas as pd
from loguru import logger

from data_fetcher import EarningsData, IncomeData, NewsData, ExtractionData
from graph_gen import fig
import plotly.io as pio

app = Flask(__name__, template_folder='website/templates', static_folder='website/static')

earnings = EarningsData()
income = IncomeData()
news = NewsData()
extraction = ExtractionData()

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    user_input = ""
    earnings_df = pd.DataFrame({})
    income_df = pd.DataFrame({})
    news_df = pd.DataFrame({})
    table_html = pd.DataFrame({})
    extraction_df = pd.DataFrame({})
    plot_html = ""
    if request.method == "POST":
        user_input = request.form.get("text_input")
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")
        if user_input is not None:
            logger.critical(start_date)
            earnings_df = earnings.get_eps(user_input, start_date_str=start_date, end_date_str=end_date)
            income_df = income.get_data(user_input)
            news_df = news.get_data(user_input)
            extraction_df = extraction.get_data(user_input)
            plot_html = pio.to_html(fig, full_html=False)

    table_html = earnings_df.to_html(classes="table table-striped", index=False)
    income_tbl_html = income_df.to_html(classes="table table-striped", index=False)
    news_tbl = news_df.to_html(classes="table table-striped", index=False)
    extraction_tbl = extraction_df.to_html(classes="table table-striped", index=False)
    start_date, end_date = None, None
    return render_template("index.html", table=table_html, user_input=user_input, income_table=income_tbl_html, news_tbl=news_tbl, extraction_tbl=extraction_tbl,  plot_html=plot_html)

    

if __name__ == '__main__':
    app.run(debug=True)