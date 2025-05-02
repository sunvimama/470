from main import app, db
import inspect

with app.app_context():
    # Get all models defined in the application
    print("Models defined in the application:")
    for name, obj in inspect.getmembers(db.Model):
        if inspect.isclass(obj) and obj.__module__ == 'main':
            print(f"- {obj.__name__}")
            # Print the attributes of each model
            for attr_name, attr_value in obj.__dict__.items():
                if not attr_name.startswith('_'):
                    print(f"  - {attr_name}: {attr_value}")
