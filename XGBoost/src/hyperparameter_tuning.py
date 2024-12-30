import xgboost as xgb
from sklearn.model_selection import GridSearchCV

def hyperparameter_tuning(X_train, y_train):
    param_grid = {
        'n_estimators': [100, 200],
        'max_depth': [3, 5, 7],
        'learning_rate': [0.01, 0.1, 0.3]
    }
    
    model = xgb.XGBClassifier(random_state=42)
    
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=3, verbose=2, n_jobs=-1)
    grid_search.fit(X_train, y_train)
    
    print("Best Parameters: ", grid_search.best_params_)
    print("Best Score: ", grid_search.best_score_)
    
    return grid_search.best_estimator_
