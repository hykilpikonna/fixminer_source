import numpy as np
import pandas as pd
import joblib
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import RandomOverSampler
def print_prec(y_test, y_pred):
    print(f'y Test Label: {np.array([int(x) for x in y_test])}')
    print(f'y Prediction: {np.array([int(x) for x in y_pred])}')

    prec, rec, f1, _ = precision_recall_fscore_support(y_test, y_pred, average='binary')
    acc = accuracy_score(y_test,y_pred)
    print(f'Precision: {prec * 100:0.1f}')
    print(f'Recall:    {rec * 100:0.1f}')
    print(f'Accuracy:  {acc*100:0.1f}')
    print(f'F1:        {f1 * 100:0.1f}')


if __name__ == '__main__':
    fm = pd.read_csv('fm-features.csv')
    d4j = pd.read_csv('d4j-features.csv')
    bdj = pd.read_csv('bdj-features.csv')
    all = pd.read_csv('data-all.absolute-features.csv')
    #X = fm.drop(columns=['LABEL','Time'],axis = 1)  # features
    #Y = fm['LABEL']  # labels
    clf = RandomForestClassifier()
    rs= RandomOverSampler(random_state=0)
    Y_all_test=all['LABEL']
    X_all_test=all.drop(columns=['LABEL','Time'],axis = 1)
    X_train, X_test, y_train, y_test = train_test_split(X_all_test, Y_all_test, test_size=0.2)
    #print(X_train)
    X_resampled, y_resampled = rs.fit_resample(X_train, y_train)
    clf.fit(X_resampled,y_resampled)

    #clf.fit(X, Y)
    # Y_bdj_test=bdj['LABEL']
    # X_bdj_test=bdj.drop(columns=['LABEL','Time'],axis = 1)
    # Y_d4j_test=d4j['LABEL']
    # X_d4j_test=d4j.drop(columns=['LABEL','Time'],axis = 1)
    # # bdj_pred=clf.predict(X_bdj_test)
    # # d4j_pred=clf.predict(X_d4j_test)
    all_pred=clf.predict(X_test)
    # # print_prec(Y_bdj_test,bdj_pred)
    # # print_prec(Y_d4j_test,d4j_pred)
    print_prec(y_test,all_pred)
    # 800 667 667 727
    joblib.dump(clf, "./random_forest.joblib")
    importance=[0.04336795, 0.11223876, 0.0586915,  0.03840793, 0.07281997, 0.06005508,
                0.08044522, 0.05864273, 0.07693864, 0.08805545, 0.05911849, 0.09307329,
                0.0981109,  0.06003408,]
    features = X_all_test.columns
    print(features)
    print(importance)
    print(clf.feature_importances_)
    # X_train, X_test, y_train, y_test = train_test_split(X_bdj_test, Y_bdj_test, test_size=0.33, random_state=42)
    # clf.fit(X_train,y_train)
    #
    # bdj_pred=clf.predict(X_test)
    # d4j_pred=clf.predict(X_d4j_test)
    # all_pred=clf.predict(X_all_test)
    # print_prec(y_test,bdj_pred)
    # print_prec(Y_d4j_test,d4j_pred)
    # print_prec(Y_all_test,all_pred)
    #
    #
    # X_train, X_test, y_train, y_test = train_test_split(X_d4j_test, Y_d4j_test, test_size=0.33, random_state=42)
    # clf.fit(X_train,y_train)
    #
    # bdj_pred=clf.predict(X_bdj_test)
    # d4j_pred=clf.predict(X_test)
    # all_pred=clf.predict(X_all_test)
    # print_prec(Y_bdj_test,bdj_pred)
    # print_prec(y_test,d4j_pred)
    # print_prec(Y_all_test,all_pred)

    # print(bdj.corr(method='spearman').sort_values(by=['LABEL'])['LABEL'])
    # print(d4j.corr(method='spearman').sort_values(by=['LABEL'])['LABEL'])
    # print(fm.corr(method='spearman').sort_values(by=['LABEL'])['LABEL'])
