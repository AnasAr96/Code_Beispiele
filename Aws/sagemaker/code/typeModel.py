from __future__ import print_function

import argparse
import os
import pandas as pd

from sklearn import tree
import joblib

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # Sagemaker specific arguments. Defaults are set in the environment variables.

    # Saves Checkpoints and graphs
    parser.add_argument('--output-data-dir', type=str, default=os.environ['SM_OUTPUT_DATA_DIR'])

    # Save model artifacts
    parser.add_argument('--model-dir', type=str, default=os.environ['SM_MODEL_DIR'])

    # Train data
    parser.add_argument('--train', type=str, default=os.environ['SM_CHANNEL_TRAIN'])
    
    


    
    args = parser.parse_args()

    
    file = os.path.join(args.train, "train_type.csv")
    dataset = pd.read_csv(file, engine="python" )

    y = dataset.iloc[:, 3:4].values
    X1 = dataset.iloc[:, 0:3]
    X2 = dataset.iloc[:, 4:]
    X = pd.concat([X1, X2], axis=1).values


    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=0)

    

    from sklearn.tree import DecisionTreeClassifier
    tree = DecisionTreeClassifier(random_state=0)
    tree.fit(X_train, y_train)

    # Print the coefficients of the trained classifier, and save the coefficients
    joblib.dump(tree, os.path.join(args.model_dir, "model.joblib"))
