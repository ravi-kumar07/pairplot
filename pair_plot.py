import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path

root = Path("datasets")
root.mkdir(exist_ok=True)

def load_dataset(path):
    df = pd.read_csv(path)
    return df

def get_categorical_columns(df):
    categorical_columns = df.select_dtypes(include=["category", "object"]).columns.tolist()
    return categorical_columns

def get_pair_plot(df, color_by=None):
    sns.set(style="ticks")
    numerical_columns = df.select_dtypes(include=["number"]).columns.tolist()
    if color_by:
        plot_data = sns.pairplot(df, vars=numerical_columns, hue=color_by)
        plot_data._legend.remove() 
    else:
        plot_data = sns.pairplot(df, vars=numerical_columns)
    return plot_data

def get_available_datasets():
    dataset_files = root.glob("*.csv")
    return [dataset.stem for dataset in dataset_files]



st.title("Explore Pair Plots")

st.sidebar.title("Manage")

available_datasets = get_available_datasets()

if not available_datasets:
    st.warning("No datasets found in the 'datasets' folder. Please upload a dataset.")
    uploaded_file = st.file_uploader("Upload a new dataset (CSV)", type="csv")
    if uploaded_file is not None:
        with open(root / uploaded_file.name, "wb") as f:
            f.write(uploaded_file.read())
        st.success(f"Uploaded and added dataset: {uploaded_file.name}")
        st.experimental_rerun()  # Restart the app to refresh the sidebar
else:
    selected_dataset = st.sidebar.selectbox("Select a dataset", available_datasets)
    df = load_dataset(root / (selected_dataset + ".csv"))
    df.columns = df.columns.str.lower()

    categorical_columns = get_categorical_columns(df)
    
    show_color_by_option = st.sidebar.checkbox("Color by a categorical column")
    if show_color_by_option:
        color_by_option = st.sidebar.selectbox("Select a categorical column to use as color by", ["None"] + categorical_columns)
        color_by = color_by_option.lower() if color_by_option != "None" else None
    else:
        color_by = None

    st.write("Upload your own dataset")
    uploaded_file = st.file_uploader("Upload a new dataset (CSV)", type="csv")
    if uploaded_file is not None:
        with open(root / uploaded_file.name, "wb") as f:
            f.write(uploaded_file.read())
        st.success(f"Uploaded and added dataset: {uploaded_file.name}")
        st.experimental_rerun()  

    st.write("Dataset Summary")
    st.write(df.head())

    st.title("Pair Plot")
    pair_plot = get_pair_plot(df, color_by)
    st.pyplot(pair_plot)

