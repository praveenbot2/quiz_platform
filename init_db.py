"""
Initialize the database and create tables
"""
from app import app, db

def main():
    print("Initializing database...")
    
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✓ Database tables created successfully")
        
        # Print table information
        print("\nCreated tables:")
        print("- patients")
        print("- health_data")
        print("- predictions")
        
    print("\nDatabase initialization complete!")
    print("You can now run: python train_models.py")

if __name__ == '__main__':
    main()
