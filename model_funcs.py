import xgboost as xgb


def model_train_predict(X_train, X_test, y_train):
    """
    returns the predictions for an xgboost model
    """
    model = xgb.XGBRegressor()

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    return predictions
