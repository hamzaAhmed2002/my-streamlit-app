import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import numpy as np

# Load dataset
dfs = [pd.read_csv(f'the-spotify-hit-predictor-dataset/dataset-of-{decade}0s.csv') for decade in ['6','7','8','9','0','1']]

for i, decade in enumerate([1960,1970,1980,1990,2000,2010]):
    dfs[i]['decade'] = pd.Series(decade, index=dfs[i].index)
        
dataset = pd.concat(dfs, axis=0).sample(frac=1.0,random_state=42).reset_index(drop=True)

# Feature extraction
numerical_features = [
    col 
    for col in dataset.columns 
    if dataset[col].dtype != "O"
]

discrete_features = [
    f 
    for f in numerical_features 
    if len(dataset[f].unique()) < 15
]

interesting_features = [
    f 
    for f in numerical_features 
    if f not in discrete_features
]



# Model training
features = interesting_features
X = dataset[features]
Y = dataset['target']
x_train, x_val, y_train, y_val = train_test_split(X, Y, test_size=0.3, random_state=42)
model = DecisionTreeClassifier()
model.fit(x_train, y_train)

# Streamlit pages
st.set_page_config(page_title="Spotify Hit Predictor", layout="wide")
pages = ["🎵 Feature Distributions", "📊 Data Overview", "🔮 Make a Prediction"]
choice = st.sidebar.selectbox("Choose a page", pages)

if choice == pages[0]:
    st.title("🎵 Feature Distributions")
    for feature in interesting_features:
        fig, ax = plt.subplots()
        dataset[feature].hist(bins=20, ax=ax)

        ax.set_xlabel(feature)
        ax.set_ylabel("Count")
        
        st.pyplot(fig)

elif choice == pages[1]:
    st.title("📊 Dataset Overview")
    st.write("### Head of dataset")

    st.dataframe(dataset.head())
    st.write("### Dataset description")

    st.dataframe(dataset.describe())
    st.write("### Correlation matrix")

    st.dataframe(dataset.drop(["track", "artist", "uri"], axis=1).corr())

elif choice == pages[2]:
    st.title("🔮 Predict if a Song Will Be a Hit")
    input_data = []
    for feature in features:
        value = st.number_input(f"{feature}", value=float(X[feature].mean()))
        input_data.append(value)

    if st.button("Predict"):

        input_array = np.array([input_data])

        prediction = model.predict(input_array)[0]

        st.success(
            f"🎯 Prediction: "
            f"{'Hit' if prediction == 1 else 'Not a Hit'}"
        )
