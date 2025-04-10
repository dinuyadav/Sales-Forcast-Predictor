import streamlit as st
import pandas as pd
import chardet
import matplotlib.pyplot as plt


st.set_page_config(page_title="Sales Data Analyzer", layout="wide")
st.title("📊 Sales Data Analyzer")

with open("style.css" ) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Upload CSV file
uploaded_file = st.file_uploader("Upload your sales CSV file", type=["csv"])

def detect_encoding(file):
    rawdata = file.read(10000)
    file.seek(0)
    result = chardet.detect(rawdata)
    return result['encoding']

if uploaded_file is not None:
    try:
        encoding = detect_encoding(uploaded_file)
        data = pd.read_csv(uploaded_file, encoding=encoding)
        st.success(f"File uploaded and read successfully using encoding: `{encoding}`")

        # Preview data
        st.subheader("🔍 Data Preview")
        st.dataframe(data.head())

        # Summary statistics
        st.subheader("📈 Summary Statistics")
        st.write(data.describe(include='all'))

        # Show columns and select for analysis
        st.subheader("🛠️ Column Selector")
        st.write("Choose columns to view insights:")
        numeric_cols = data.select_dtypes(include='number').columns.tolist()
        all_cols = data.columns.tolist()

        x_axis = st.selectbox("Select X-axis column (e.g., Date/Product)", all_cols)
        y_axis = st.selectbox("Select Y-axis column (e.g., Sales/Revenue)", numeric_cols)

        if x_axis and y_axis:
            st.subheader("📊 Basic Visualization")
            grouped_data = data.groupby(x_axis)[y_axis].sum().sort_values(ascending=False)

            st.bar_chart(grouped_data)

            # Show top 5
            st.write(f"Top 5 `{x_axis}` by `{y_axis}`")
            st.dataframe(grouped_data.head())

    except Exception as e:
        st.error(f"⚠️ Error reading the file: {e}")
else:
    st.info("Please upload a CSV file to start the analysis.")
