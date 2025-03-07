import streamlit as st
import pandas as pd

# Streamlit UI
st.title("Custom Sales Report Generator")
st.markdown("Upload your sales report and generate insights including outstanding balances.")

# File uploader for sales report
uploaded_file = st.file_uploader("Upload Sales Report (Excel)", type=["xlsx"])

# Option for SKU filtering
sku_option = st.radio("Do you want to filter specific SKUs?", ("No", "Yes - Upload a file", "Yes - Enter manually"))

sku_list = None
if sku_option == "Yes - Upload a file":
    sku_file = st.file_uploader("Upload SKU List (CSV)", type=["csv"])
    if sku_file:
        sku_list = pd.read_csv(sku_file)['SKU'].tolist()
        st.success(f"Loaded {len(sku_list)} SKUs from file.")

elif sku_option == "Yes - Enter manually":
    sku_text = st.text_area("Enter SKUs separated by commas")
    if sku_text:
        sku_list = [sku.strip() for sku in sku_text.split(",")]
        st.success(f"Loaded {len(sku_list)} SKUs from manual input.")

if uploaded_file:
    # Load Excel file
    xls = pd.ExcelFile(uploaded_file)

    try:
        # Load sheets
        data_df = pd.read_excel(xls, sheet_name="Data")
        oos_df = pd.read_excel(xls, sheet_name="OOS")

        st.success("Files loaded successfully!")

        # Filter SKUs if provided
        if sku_list:
            data_df = data_df[data_df['SKU'].isin(sku_list)]
            st.info(f"Filtered {len(data_df)} records based on selected SKUs.")

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
