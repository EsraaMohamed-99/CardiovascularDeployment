from Scripts import Imports
import joblib
def Prediction(df):
	# Load model
	with open("pklFiles/best_lgbm_model.pkl", "rb") as f:
		best_lgbm_model = joblib.load(f)

	# 7. Predictions on test set
	y_pred = best_lgbm_model.predict(df)
	return y_pred