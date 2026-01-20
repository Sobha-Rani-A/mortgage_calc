from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        try:
            amount = float(request.form.get('amount'))
            term = int(request.form.get('term'))
            rate = float(request.form.get('rate')) / 100 / 12
            type = request.form.get('type')
            months = term * 12

            if type == 'repayment':
                # Standard Mortgage Formula: M = P [ i(1 + i)^n ] / [ (1 + i)^n – 1 ]
                monthly = amount * (rate * (1 + rate)**months) / ((1 + rate)**months - 1)
            else:
                # Interest Only: M = P * i
                monthly = amount * rate
            
            result = {
                "monthly": round(monthly, 2),
                "total": round(monthly * months, 2),
                "currency": request.form.get('currency')
            }
        except (ValueError, ZeroDivisionError):
            result = "error"

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)