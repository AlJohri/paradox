from sklearn.cross_validation import KFold
from metrics import pearson, mse
from pipeline import pipeline
import k_neighbors_regressor
import numpy as np
import similarity
import parser


def benchmark(X_train, y_train, transformers, estimator, n_folds=10):
    skf = KFold(len(y_train), n_folds=n_folds, shuffle=True, random_state=0)
    p = pipeline(transformers=transformers, estimator=estimator)
    fold, pcs, rmses = 1, [], []
    print('Starting cross validation: num_fold={}'.format(n_folds))
    for train_index, test_index in skf:
        print('Evaluating fold {}'.format(fold))
        X_train_fold = [X_train[i] for i in train_index]
        y_train_fold = [y_train[i] for i in train_index]
        X_test_fold = [X_train[i] for i in test_index]
        y_test_fold = [y_train[i] for i in test_index]
        p.fit(X_train_fold, y_train_fold)
        y_pred_fold = p.predict(X_test_fold)
        pcs.append(pearson(y_test_fold, y_pred_fold))
        rmses.append(mse(y_test_fold, y_pred_fold))
        fold = fold + 1
        report(pcs, rmses, y_pred_fold, n_folds)


def report(correlations, errors, y_pred_fold, n_folds=None):
    print('{} {}-fold CV Report {}'.format('*' * 11, n_folds, '*' * 11))
    print("PC:\t\t\t%0.2f\t(+/- %0.2f)" % (np.mean(correlations),
                                           np.std(correlations) * 2))
    print("RMSE:\t\t\t%0.2f\t(+/- %0.2f)" % (np.mean(errors),
                                             np.std(errors) * 2))
    print("Predictions mean:\t%0.2f" % (np.mean(y_pred_fold)))
    print("Predictions var:\t%0.2f" % (np.var(y_pred_fold)))
    print('{}'.format('*' * 40))

pairs = parser.parse(mode="train")
X = [pair[0] for pair in pairs]
y = [pair[1] for pair in pairs]
transformer = similarity.build()
estimator = k_neighbors_regressor.build(n_neighbors=4)
#benchmark(X, y, [transformer], estimator, n_folds=2)
p = pipeline(transformers=[transformer], estimator=estimator)
p.fit(X, y)


def test(model=None, categories=[]):
    print "Testing on Category {}".format(categories)
    test_pairs = parser.parse(mode="test", categories=categories)
    X = [pair[0] for pair in test_pairs]
    y = [pair[1] for pair in test_pairs]
    y_pred = p.predict(X)
    pcs = [pearson(y, y_pred)]
    rmses = [mse(y, y_pred)]
    report(pcs, rmses, y_pred, 0)

test(p, categories=["answer-answer"])
test(p, categories=["question-question"])
test(p, categories=["headlines"])
test(p, categories=["postediting"])
test(p, categories=["plagiarism"])
