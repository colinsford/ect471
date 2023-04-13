from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Colin'}
    return '''
<html>
    <head>
        <title>Home Page - TFord Photo</title>
    </head>
    <body>
        <h1>Hello, ''' + user['username'] + '''!</h1>
    </body>
</html>'''