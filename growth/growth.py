import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Page Config
st.set_page_config(page_title="Data Sweeper", layout='wide')

# Custom CSS for Styling
st.markdown(
    """
    <style>
    .stApp {
        background-color: black;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and Description
st.title("📊 Datasweeper Sterling Integration By Mrs Asif")
st.write("Transform your files between CSV and Excel format with built-in data cleaning and visualization.")

# File Uploader
uploaded_files = st.file_uploader("📂 Upload your files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()  # Extracts file extension
        
        # Read File Based on Type
        if file_ext == "csv":
            df = pd.read_csv(file)
        elif file_ext == "xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"❌ Unsupported file type: {file_ext}")
            continue  # Skip this file and process the next one

        # Display File Details
        st.subheader(f"🔍 Preview - {file.name}")
        st.dataframe(df.head())

        # Data Cleaning Options
        st.subheader("🧹 Data Cleaning Options")
        
        if st.checkbox(f"Clean the data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"🚫 Remove Duplicates from {file.name}"):
                    df = df.drop_duplicates()  # Fixed inplace issue
                    st.success("✅ Duplicates removed successfully!")

            with col2:
                if st.button(f"🛠️ Fill Missing Values in {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    if not numeric_cols.empty:
                        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                        st.success("✅ Missing values have been filled!")
                    else:
                        st.warning("⚠️ No numeric columns found to fill missing values.")

        # Column Selection
        st.subheader("📌 Select Columns to Keep")
        selected_columns = st.multiselect(f"Choose columns for {file.name}", df.columns, default=df.columns)
        df = df[selected_columns] if selected_columns else df  # Prevent empty selection

        # Data Visualization
        st.subheader("📊 Data Visualization")
        numeric_df = df.select_dtypes(include=['number'])  # Select only numeric columns
        
        if st.checkbox(f"Show Visualization for {file.name}"):
            if numeric_df.shape[1] >= 1:
                st.bar_chart(numeric_df)  # Display bar chart with all numeric data
            else:
                st.warning("⚠️ No numeric columns available for visualization.")

        # Conversion Options
        st.subheader("🔄 Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()

            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"

            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)  # Fixed incorrect .to.to_excel() issue
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)

            # Provide Download Button
            st.download_button(
                label=f"⬇️ Download {file_name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

    st.success("✅ All files processed successfully!")
