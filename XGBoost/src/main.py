import time
import joblib
from data_preprocessing import load_data, preprocess_data
from model import build_model, train_model, evaluate_model
from hyperparameter_tuning import hyperparameter_tuning
from utils import save_predictions

def save_model(model, filename):
    joblib.dump(model, filename)
    print(f"模型已保存至 {filename}")

def load_model(filename):
    model = joblib.load(filename)
    print(f"模型已从 {filename} 加载")
    return model

def main():
    # 载入数据
    train_df, test_df = load_data("D:/Desktop/XGBoostF/data/train_vec.csv", "D:/Desktop/XGBoostF/data/test_vec.csv")
    
    # 数据预处理
    X_train, X_val, y_train, y_val, test_data = preprocess_data(train_df, test_df)
    
    # 超参数调优
    print("正在调优超参数...")
    best_model = hyperparameter_tuning(X_train, y_train)
    
    # 训练模型
    print("正在训练模型...")
    model = build_model()
    trained_model = train_model(model, X_train, y_train)

    # 保存模型
    save_model(trained_model, "trained_model.joblib")
    
    # 评估模型
    print("正在评估模型...")
    evaluate_model(trained_model, X_val, y_val)
    
    # 保存预测结果
    save_predictions(trained_model, test_data, "data/submission.csv")
    
if __name__ == "__main__":
    start_time = time.time()
    main()
    print(f"执行时间: {time.time() - start_time:.2f} 秒")
