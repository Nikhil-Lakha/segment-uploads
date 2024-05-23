import streamlit as st
import pandas as pd
from ftplib import FTP

# Title of the Streamlit app
st.title("Upload a TXT File and Display as DataFrame")

# Sidebar for file upload and options
st.sidebar.header("Upload and Options")

# Upload file in the sidebar
uploaded_file = st.sidebar.file_uploader("Choose a TXT file", type="txt")

# Segment name input in the sidebar
segment_name = st.sidebar.text_input("Segment Name", value="")

# FTP details
ftp_host = "ftp3.omniture.com"
ftp_port = 21
ftp_login = "vodacomdlsvodacomfinanci_7493522"
ftp_password = "Bt0xTAlG"

if uploaded_file is not None:
    try:
        # Read the file into a DataFrame with tab delimiter
        df = pd.read_csv(uploaded_file, delimiter='\t')
        
        # Check if 'user_ids' column exists
        if 'user_ids' in df.columns:
            user_ids = df['user_ids'].tolist()
        else:
            user_ids = ["" for _ in range(len(df))]

        # Create the initial DataFrame with the specified headers and rows
        initial_data = {
            "## SC": ["## SC", "## SC", "Key"] + user_ids,
            "SiteCatalyst SAINT Import File": [
                "'## SC' indicates a SiteCatalyst pre-process header. Please do not remove these lines.",
                "D:2024-01-11 02:06:57",
                "Segment Name"]  + [segment_name for _ in range(len(df))], 
            "v:2.1": ["", "A:0:0", ""] + ["" for _ in range(len(df))]
        }
        initial_df = pd.DataFrame(initial_data)
        
        # Drop the original 'user_ids' column if it exists
        if 'user_ids' in df.columns:
            df = df.drop(columns=['user_ids'])
        
        # Concatenate the initial DataFrame with the main DataFrame
        final_df = pd.concat([initial_df, df], ignore_index=True)
        
        # Display the DataFrame
        st.write("DataFrame:")
        st.dataframe(final_df)
        
        # Upload to FTP
        if st.button("Upload DataFrame to FTP"):
            # Convert DataFrame to tab-delimited .txt file
            csv = final_df.to_csv(sep='\t', index=False)
            file_content = csv.encode()
            
            # Connect to FTP server
            with FTP() as ftp:
                ftp.connect(ftp_host, ftp_port)
                ftp.login(ftp_login, ftp_password)
                
                # Change to the appropriate directory
                ftp.cwd("path/to/directory")
                
                # Upload the file
                with ftp.storlines("STOR dataframe.txt", open("dataframe.txt", "rb")) as f:
                    f.write(file_content)
                
            st.success("File uploaded successfully!")
        
    except Exception as e:
        st.error(f"Error: {e}")
