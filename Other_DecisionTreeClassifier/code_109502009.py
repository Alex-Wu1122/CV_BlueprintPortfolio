import sklearn.metrics
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
class Node:
    """Decision tree node"""
    def __init__(self, entropy, num_samples, num_samples_per_class, predicted_class, num_errors, alpha=float("inf")):
        self.entropy = entropy  # the entropy of current node
        self.num_samples: int = num_samples
        self.num_samples_per_class: list[int] = num_samples_per_class
        self.predicted_class = predicted_class  # the majority class of the split group
        self.feature_index = -1  # the feature index we used to split the node
        self.threshold = 0  # for binary split
        self.left: Node = None  # left child node
        self.right: Node = None  # right child node
        self.num_errors: int = num_errors  # error after cut
        self.alpha: int = alpha  # each node alpha


class DecisionTreeClassifier:
    def __init__(self, max_depth=4):
        self.max_depth = max_depth
        self.node_number = 0

    def _entropy(self, sample_y):
        entropy = 0
        if sample_y.size:
            p = []
            for v in np.bincount(sample_y):
                p.append(v/sample_y.size)
            for pi in p:
                if (pi!=0):
                    entropy+=-1*(pi*np.log2(pi))
        # sample_y epresent the label of node
        # entropy = -sum(pi * log2(pi))
        return entropy

    def _feature_split(self, X, y):
        # Returns:
        #  best_idx: Index of the feature for best split, or None if no split is found.
        #  best_thr: Threshold to use for the split, or None if no split is found.
        m = y.size
        if m <= 1:
            return None, None

        # Entropy of current node.
        best_criterion = self._entropy(y)
        max_info=-1
        best_idx, best_thr = None, None
        for idx in range(X.shape[1]):
            feature = X[:, idx]
            thrs = np.unique(feature)
            for thr in thrs:
                
                left_idx=[]
                right_idx=[]
                for i in range(feature.size):
                    if feature[i]<=thr:
                        left_idx.append(i)
                    elif feature[i]>thr:
                        right_idx.append(i)
                lm = len(left_idx)/feature.size
                rm = len(right_idx)/feature.size
                le = self._entropy(y[left_idx]) 
                re = self._entropy(y[right_idx])
                expected_info = lm * le + rm * re
                info = best_criterion - expected_info
                if info > max_info:
                    max_info = info
                    best_idx = idx
                    best_thr = thr

        return best_idx, best_thr

    def _build_tree(self, X, y, depth:int=0):
        num_samples_per_class = [np.sum(y == i) for i in range(self.n_classes)]
        predicted_class = np.argmax(num_samples_per_class)
        correct_label_num = num_samples_per_class[predicted_class]
        num_errors = y.size - correct_label_num
        node = Node(
            entropy = self._entropy(y),
            num_samples=y.size,
            num_samples_per_class=num_samples_per_class,
            predicted_class=predicted_class,
            num_errors=num_errors
        )
        num_classes = np.unique(y).size
        if depth < self.max_depth and num_errors > 0:
            idx, thr = self._feature_split(X, y)
            if idx is not None:
                node.feature_index =idx
                node.threshold =thr
                leftidx=[]
                rightidx=[]
                for i in range(X[:,idx].size):
                    if X[:,idx][i]<=thr:
                        leftidx.append(i)
                    elif X[:,idx][i]>thr:
                        rightidx.append(i)
                leftX = X[leftidx, :]
                leftY = y[leftidx]
                rightX = X[rightidx, :]
                rightY = y[rightidx]
                node.left = self._build_tree(leftX, leftY, depth+1)
                node.right = self._build_tree(rightX, rightY, depth+1)
        return node

    def fit(self,X,Y):
        self.node_number = 0
        self.n_classes = np.unique(Y).size
        self.data_num = np.size(X,0)
        self.feature_num = np.size(X,1)
        self.root = self._build_tree(X, Y)
        # Fits to the given training data

    def predict(self,X):
        pred = []
        for x in X:
            pred.append(self.recursive_trace(x,self.root).predicted_class)

        return pred

    def recursive_trace(self, x, root):
        if root:
            if root.right== None and root.left== None:
                return root
            if x[root.feature_index] <= root.threshold:
                return self.recursive_trace(x, root.left)
            return self.recursive_trace(x, root.right)

    def _find_leaves(self, root):
        if root.right== None and root.left== None:
            return 1
        sum = self._find_leaves(root.left) + self. _find_leaves(root.right)
        return sum
        ## find each node child leaves number

    def _error_before_cut(self, root):
        if root is None:
            return 0
        if root.right== None and root.left== None:
            return root.num_errors
        ##  return error before post-pruning
        sum = self._error_before_cut(root.right) + self._error_before_cut(root.left)
        return sum

    def _compute_alpha(self, root):
        ## Compute each node alpha
        # alpha = (error after cut - error before cut) / (leaves been cut - 1)
        before = self._error_before_cut(root)
        leaves = self._find_leaves(root)
        alpha = (root.num_errors - before)/(leaves-1)
        root.alpha = alpha
        return alpha

    def _find_min_alpha(self, root):
        if not (root.right== None and root.left== None):
            self.MinAlpha = float("inf")
            alpha = self._compute_alpha(root)
            if alpha < self.MinAlpha:
                self.MinAlpha = alpha
                self.prune_node = root
            if root.left:
                self._find_min_alpha(root.left)
            if root.right:
                self._find_min_alpha(root.right)

        ##  Search the Decision tree which have minimum alpha's node

    def _prune(self):
        self.prune_node= None
        self._find_min_alpha(self.root)
        self.prune_node.left = None
        self.prune_node.right = None


def load_train_test_data(test_ratio=.3, random_state = 1):
    df = pd.read_csv('./car.data', names=['buying', 'maint',
                     'doors', 'persons', 'lug_boot', 'safety', 'target'])
    X = df.drop(columns=['target'])
    X = np.array(X.values)
    y = np.array(df['target'].values)
    label = np.unique(y) 
    #  label encoding
    for i in range(len(y)):
        for j in range(len(label)):
            if y[i] == label[j]:
                y[i] = j
                break
    y = y.astype('int')
    for i in range(len(X)):
        for j in range(len(X[i])):
            X[i][j] = ord(X[i][j][0])
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size = test_ratio, random_state=random_state, stratify=y
    )
    return X_train, X_test, y_train, y_test


def accuracy_report(X_train_scale, y_train, X_test_scale, y_test,max_depth=7):
    tree = DecisionTreeClassifier(max_depth=max_depth)
    tree.fit(X_train_scale, y_train)
    pred = tree.predict(X_train_scale)

    print(" tree train accuracy: %f"
         % (sklearn.metrics.accuracy_score(y_train, pred )))
    pred = tree.predict(X_test_scale)
    print(" tree test accuracy: %f"
       % (sklearn.metrics.accuracy_score(y_test, pred )))

    for i in range(10):
        print("=============Cut=============")
        tree._prune()
        pred = tree.predict(X_train_scale)
        print(" tree train accuracy: %f"
              % (sklearn.metrics.accuracy_score(y_train, pred)))
        pred = tree.predict(X_test_scale)
        print(" tree test accuracy: %f"
              % (sklearn.metrics.accuracy_score(y_test, pred)))
def main():
    X_train, X_test, y_train, y_test = load_train_test_data(test_ratio=.3,random_state = 1)
    accuracy_report(X_train, y_train,X_test,y_test,max_depth=14)


if __name__ == "__main__":
    main()
