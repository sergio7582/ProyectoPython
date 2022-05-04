from datetime import datetime
from flask import render_template
from flask import Flask


# Create an instance of the Flask class that is the WSGI application.
# The first argument is the name of the application module or package,
# typically __name__ when using a single module.
app = Flask(__name__)

# Flask route decorators map / and /hello to the hello function.
# To add other resources, create functions that generate the page contents
# and add decorators to define the appropriate resource locators for them.

@app.route('/')
@app.route('/Index')
def Index():
    now = datetime.now()
    formatted_now = now.strftime("%A, %d %B, %Y at %X")
    
    # Render the page
    return render_template(
        "Home.html",
        content = formatted_now,
        message = "Esto esta chido xd "
        )


if __name__ == '__main__':
    # Run the app server on localhost:4449
    app.run('localhost', 4449)
