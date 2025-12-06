from sklearn.metrics import roc_auc_score, accuracy_score

class ModelEvaluator:

    def evaluate(self, model, X_train, y_train, X_valid, y_valid):
        preds_train = model.predict_proba(X_train)[:,1]
        preds_valid = model.predict_proba(X_valid)[:,1]

        return {
            "auc_train": roc_auc_score(y_train, preds_train),
            "auc_valid": roc_auc_score(y_valid, preds_valid),
            "acc_train": accuracy_score(y_train, preds_train > 0.5),
            "acc_valid": accuracy_score(y_valid, preds_valid > 0.5),
            "gap_auc": roc_auc_score(y_train, preds_train) - roc_auc_score(y_valid, preds_valid)
        }
