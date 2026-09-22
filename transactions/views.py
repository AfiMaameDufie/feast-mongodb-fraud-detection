from django.http import JsonResponse
from transactions.feast_client import get_latest_transaction_features

# From training/train_model.py -- mean and std of `amount` on training data.
TRAIN_MEAN_AMOUNT = 40.6112153107239
TRAIN_STD_AMOUNT = 26.347826549161585
Z_SCORE_THRESHOLD = 2.0


def score_transaction(request, user_id: int):
    features = get_latest_transaction_features(user_id)

    amount = features.get("amount")
    if amount is None:
        return JsonResponse({"error": f"No features found for user_id {user_id}"}, status=404)

    z_score = (amount - TRAIN_MEAN_AMOUNT) / TRAIN_STD_AMOUNT
    is_potentially_fraudulent = abs(z_score) > Z_SCORE_THRESHOLD

    return JsonResponse({
        "user_id": user_id,
        "amount": amount,
        "category": features.get("category"),
        "location": features.get("location"),
        "z_score": round(z_score, 3),
        "is_potentially_fraudulent": is_potentially_fraudulent,
    })