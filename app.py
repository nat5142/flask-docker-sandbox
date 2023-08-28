from src.main import create_app

# Create application in factory method
app = create_app()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
