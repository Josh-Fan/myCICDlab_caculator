from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!doctype html>
<html>
<head><title>Web Calculator</title></head>
<body>
  <h2>Simple Calculator</h2>
  <form method="post">
    <input type="number" name="num1" step="any" required>
    <select name="operation">
      <option value="add">+</option>
      <option value="subtract">−</option>
      <option value="multiply">×</option>
      <option value="divide">÷</option>
    </select>
    <input type="number" name="num2" step="any" required>
    <button type="submit">Calculate</button>
  </form>
  {% if result is not none %}
    <h3>Result: {{ result }}</h3>
  {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def calculator():
    result = None
    if request.method == "POST":
        try:
            num1 = float(request.form["num1"])
            num2 = float(request.form["num2"])
            op = request.form["operation"]

            if op == "add":
                result = num1 + num2
            elif op == "subtract":
                result = num1 - num2
            elif op == "multiply":
                result = num1 * num2
            elif op == "divide":
                result = num1 / num2 if num2 != 0 else "Error: Division by zero"
        except Exception as e:
            result = f"Error: {str(e)}"
    return render_template_string(HTML_TEMPLATE, result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)