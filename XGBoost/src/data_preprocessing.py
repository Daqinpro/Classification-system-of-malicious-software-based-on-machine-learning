import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical

def load_data(train_path, test_path):
    # 加载训练和测试数据
    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)
    
    return train_df, test_df

def preprocess_data(train_df, test_df):
    # 处理训练数据
    X = train_df.drop(["Id", "Class"], axis=1).values
    y = to_categorical(train_df["Class"] - 1)  # 将类别标签转换为 one-hot 编码
    
    # 划分训练集和验证集
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, stratify=train_df["Class"], test_size=0.3, random_state=42
    )

    # 处理测试数据
    test_data = test_df.drop("Id", axis=1).values
    
    return X_train, X_val, y_train, y_val, test_data
