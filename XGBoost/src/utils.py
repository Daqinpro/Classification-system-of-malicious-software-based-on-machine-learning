import pandas as pd

def save_predictions(model, test_data, output_path):
    # 对测试集进行预测
    predictions = model.predict_proba(test_data)
    # 保存结果
    output = pd.DataFrame(predictions, columns=[f"Prediction{i}" for i in range(1, 10)])
    output["Id"] = range(1, len(test_data) + 1)
    output.to_csv(output_path, index=False)
    print(f"Predictions saved to {output_path}")
