from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    gratuity = None
    if request.method == "POST":
        salary = float(request.form.get("salary", 0))
        joining_date_str = request.form.get("joining_date")
        leaving_date_str = request.form.get("leaving_date")
        limit_option = request.form.get("limit_option")

        # Parse dates
        joining_date = datetime.strptime(joining_date_str, "%Y-%m-%d")
        leaving_date = datetime.strptime(leaving_date_str, "%Y-%m-%d")

        # Calculate number of years (rounded according to gratuity rules)
        total_service_days = (leaving_date - joining_date).days
        years_of_service = total_service_days / 365

        # Round off: more than 6 months counts as 1 full year
        if (years_of_service - int(years_of_service)) >= 0.5:
            years_of_service = int(years_of_service) + 1
        else:
            years_of_service = int(years_of_service)

        # Calculate gratuity
        gratuity = (salary * 15 * years_of_service) / 26

        # Apply limit if selected
        if limit_option == "limited":
            gratuity = min(gratuity, 2000000)  # 20 lakh maximum

    return render_template("index.html", gratuity=gratuity)

if __name__ == "__main__":
    app.run(debug=True)
