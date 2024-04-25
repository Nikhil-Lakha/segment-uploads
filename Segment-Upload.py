import streamlit as st
import pandas as pd
from ftplib import FTP
import io

# Function to upload file to FTP server
def upload_to_ftp(host, port, login, password, file_content, file_name):
    ftp = FTP()
    ftp.connect(host, port)
    ftp.login(login, password)
    ftp.storbinary(f"STOR {file_name}", io.BytesIO(file_content.encode()))
    ftp.quit()

def main():
    st.sidebar.title("Options")
    file_uploaded = st.sidebar.file_uploader("Upload a .txt file", type=["txt"])
    additional_text = st.sidebar.text_input("Enter additional text")

    if file_uploaded:
        st.sidebar.write("File uploaded successfully!")
        st.sidebar.write("File name:", file_uploaded.name)
        
        # Read the text file
        text = file_uploaded.getvalue().decode("utf-8")
        
        # Split text into lines
        lines = text.split("\n")
        
        # Create a dataframe from the lines
        df = pd.DataFrame(lines, columns=["## SC"])
        
        # Add additional text to the second column
        df["SiteCatalyst SAINT Import File"] = additional_text
        df["v:2.1"] = ""

        # Insert "## SC" in the first three rows
        df.iloc[0,0] = "## SC"
        df.iloc[1,0] = "## SC"
        df.iloc[2,0] = "Key"

        df.iloc[0,1] = "'## SC' indicates a SiteCatalyst pre-process header. Please do not remove these lines."
        df.iloc[1,1] = "D:2024-01-11 02:06:57"
        df.iloc[2,1] = "Segment Name"
        
        df.iloc[0,2] = ""
        df.iloc[1,2] = "A:0:0"
        df.iloc[2,2] = ""
        
        # Show dataframe
        st.write("DataFrame:")
        st.write(df)
        
        # Button to upload file to FTP
        if st.button("Upload to FTP"):
            try:
                upload_to_ftp(
                    host="ftp3.omniture.com",
                    port=21,  # Change to the appropriate port number
                    login="vodacomdlsvodacomfinanci_7493522",
                    password="Bt0xTAlG",
                    file_content=df.to_csv(sep="\t", index=False, header=False),
                    file_name=file_uploaded.name
                )
                st.success("File uploaded successfully to FTP!")
            except Exception as e:
                st.error(f"Error uploading file to FTP: {str(e)}")

if __name__ == "__main__":
    main()