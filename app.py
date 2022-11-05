from src.main import create_app

# Create application in factory method
app = create_app()


@app.route('/')
def hello():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
