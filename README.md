# Fraud Detection with Feast + MongoDB

A hands-on example pipeline that combines **Django** + **django-mongodb-backend**, **Feast**, and **MongoDB** to detect potentially fraudulent transactions.

- Transactions are stored in MongoDB through the Django ORM (`transactions` app).
- Feast defines and manages `transaction_features` (`amount`, `category`, `location`), using a local Parquet file as the offline store and **MongoDB as the online store**.
- A simple z-score model (`training/train_model.py`) is trained on historical features pulled from Feast.
- Features are materialized into MongoDB via `feast materialize`, and a Django view (`transactions/views.py`) scores transactions in real time by looking up each user's latest materialized features.

## Quickstart

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Create a .env file with SECRET_KEY, MONGODB_URI, and DB_NAME (see tutorial.md)

python data/generate_transactions.py
python manage.py migrate
python manage.py load_transactions

cd feature_repo/feature_repo
feast apply
feast materialize 2020-01-01T00:00:00 2026-08-01T00:00:00
cd ../..

python manage.py runserver
```

Then request a fraud score:

```bash
curl http://127.0.0.1:8000/score/2/
```
