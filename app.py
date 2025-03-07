import streamlit as st
import pandas as pd

# Streamlit UI
st.title("Custom Sales Report Generator")
st.markdown("Upload your sales report and generate insights including outstanding balances.")

# File uploader
uploaded_file = st.file_uploader("Upload Sales Report (Excel)", type=["xlsx"])

if uploaded_file:
    # Load Excel file
    xls = pd.ExcelFile(uploaded_file)

    # Load sheets
    try:
        data_df = pd.read_excel(xls, sheet_name="Data")
        oos_df = pd.read_excel(xls, sheet_name="OOS")
        
        st.success("Files loaded successfully!")

        # Display data preview
        st.subheader("Sales Data Preview")
        st.dataframe(data_df.head())

        st.subheader("Outstanding Orders Preview")
        st.dataframe(oos_df.head())

        # Merge Data with OOS
        merged_df = data_df.merge(
            oos_df[['Simple SKU', 'Actual Outstanding Balance', 'Estimated Delivery Date']],
            left_on='SKU', right_on='Simple SKU', how='left'
        )

        # Drop redundant column
        merged_df.drop(columns=['Simple SKU'], inplace=True)

        # Display results
        st.subheader("Final Sales Report with Outstanding Balances")
        st.dataframe(merged_df)

        # Download button
        @st.cache_data
        def convert_df(df):
            return df.to_csv(index=False).encode('utf-8')

        csv = convert_df(merged_df)
        st.download_button(
            label="Download Report as CSV",
            data=csv,
            file_name="sales_report_with_outstanding_balances.csv",
            mime="text/csv",
        )

    except Exception as e:
        st.error(f"Error processing file: {e}")

