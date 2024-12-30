import xgboost as xgb
from sklearn.metrics import accuracy_score, log_loss, confusion_matrix
import pandas as pd
from sklearn.metrics import roc_auc_score, f1_score, classification_report
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelBinarizer
from sklearn.metrics import roc_curve

def build_model():
    # 初始化 XGBoost 分类器
    model = xgb.XGBClassifier(random_state=42, n_jobs=-1)
    return model

def train_model(model, X_train, y_train):
    # 训练模型
    model.fit(X_train, y_train)
    return model


def evaluate_model(model, X_val, y_val):
    # 预测类别标签的概率
    y_pred = model.predict(X_val)
    
    # 将 y_val 和 y_pred 转换为整数类标签
    y_val_labels = y_val.argmax(axis=1)  # 转换为整数类标签
    y_pred_labels = y_pred.argmax(axis=1)  # 转换为整数类标签
    
    # 计算准确率
    accuracy = accuracy_score(y_val_labels, y_pred_labels)
    
    # 计算对数损失
    loss = log_loss(y_val, y_pred)
    
    # 混淆矩阵
    confusion = confusion_matrix(y_val_labels, y_pred_labels)
    
    # 计算 AUC-ROC
    lb = LabelBinarizer()
    y_val_bin = lb.fit_transform(y_val_labels)
    y_pred_proba = model.predict_proba(X_val)  # 获取预测的概率
    auc = roc_auc_score(y_val_bin, y_pred_proba, multi_class='ovr')  # multi_class='ovr' 适用于多分类
    
    # 计算 F1-score
    f1 = f1_score(y_val_labels, y_pred_labels, average='weighted')  # 'weighted' 适用于多分类
    
    # 输出评估结果
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Log Loss: {loss:.4f}")
    print(f"AUC-ROC: {auc:.4f}")
    print(f"F1-score: {f1:.4f}")
    print(f"Classification Report:\n{classification_report(y_val_labels, y_pred_labels)}")
    print(f"Confusion Matrix:\n{confusion}")
    
    # 绘制 ROC 曲线
    plot_roc_curve(y_val_bin, y_pred_proba, lb.classes_)

    return accuracy, loss, auc, f1, confusion


def plot_roc_curve(y_true, y_pred, classes):
    # 绘制每一类的 ROC 曲线
    plt.figure(figsize=(10, 8))
    for i, class_name in enumerate(classes):
        fpr, tpr, _ = roc_curve(y_true[:, i], y_pred[:, i])
        plt.plot(fpr, tpr, label=f'{class_name} (AUC = {roc_auc_score(y_true[:, i], y_pred[:, i]):.2f})')

    plt.plot([0, 1], [0, 1], 'k--')  # 随机猜测的对角线
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curve for Each Class')
    plt.legend(loc='lower right')
    plt.show()

