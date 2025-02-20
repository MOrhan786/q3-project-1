import streamlit as st
import pandas as pd
import os
from io import BytesIO
# page config
st.set_page_config(page_title="Data Sweeper",layout='wide')

# custom css
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
# title and description
st.title("📊 Datasweeper Sterling Integration By Mrs Asif")
st.write("Transform your files between CSV and Excel format with built-in data cleaning and visualization creating the project for quarter 3!. ")

# upload file
uploaded_files = st.file_uploader("📂 Upload  your files(accepts CSV or Excel ):", type=["csv","xlsx"], accept_multiple_files=(True))

if uploaded_files:
    for file in uploaded_files:
    file_ext = os.path.splitext(file.name)[-1].lower()  # Extracts file extension
     
     if file_ext == ".csv":
        df = pd.read_csv(file)
     elif file_ext == "xlsx":
        df = pd.read_excel(file)
     else:
            st.error(f"unsupported file type: {file_ext}")
            continue

            # file details
            st.write("📜 Preview the head of the Dataframe")
            st.dataframe(df.head())

            # data cleaning options
            st.subheader(" 🧹Data Cleaning Options")
            if st.checkbox(f"Clean the data for {file.name}"):
               col1, col2 = st.columns(2)

               with col1:
                  if st.button(f"🚫 Remove duplicate from the file :{file.name}"):
                     df.drop_duplicates(inplace=True)
                    st.write(" ✅ Duplicates  removed successfully!")

               with col2:
                  if st.button("Fill missing values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write(" ✅ Missing values have been filled!")

                    st.subheader("📌 Select the columns to keep")
                    columns = st.multiselect(f"Chose columns for {file.name}",df.columns, default=df.columns)
                    df = df[columns]
                    
                    # data visualization
                    st.subheader("📊  Data Visualization")
                    if st.checkbox(f"Show visualization for {file.name}"):
                       st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

                    #    Conversion options
                     st.subheader("🔄 Conversion Options")
                     Conversion_type = st.radio("Cnvert {file.name} to:", ["CSV","Excel"], key=file.name)
                     if st.button(f"Convert  {file.name}"):
                        buffer = BytesIO()
                        if Conversion_type == "CSV":
                            df.to_csv(buffer,index=False)
                            file_name = file.name.replace(file_ext, ".csv")
                            mime_type = "text/csv"

                            elif conversion_type == "Excel":
                                df.to.to_excel(buffer, index=False)
                                file_name = file.name.replace(file_ext, ".xlsx")
                                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                                buffer.seek(0)

                                st.download_button(
                                    label=f"Download {file_name} as {Conversion_type}",
                                    data=buffer,
                                    file_name=file_name,
                                    mime=mime_type
                                    )
        st.success("✅ All files proccessed successfully!")
                           
                    
                        














             
                   
                








