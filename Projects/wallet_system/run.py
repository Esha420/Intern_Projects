from wallet_app import create_app, db
from wallet_app.models.user import User
from wallet_app.models.transaction import Transaction

app = create_app()

def init_db():
    with app.app_context():
        db.create_all()
        
        if not User.query.first():
            test_user = User(
                username='admin',
                email='admin@wallet.com',
                password=User.generate_hash('admin123'),
                tier='premium',
                balance=5000.00,
                kyc_verified=True
            )
            db.session.add(test_user)
            db.session.commit()
            print("Database initialized with test user!")

if __name__ == '__main__':
    init_db()
    print("Database setup complete!")
    app.run(debug=True)