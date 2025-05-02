# services/excel_reader.py

import pandas as pd
import os
import json
class ExcelReader:
    def __init__(self, data_folder='data'):
        self.data_folder = data_folder
        self.file_path = self.find_file()
        self.dataframe = None

    def find_file(self):
        """Finds the first Excel file in the data folder."""
        if not os.path.exists(self.data_folder):
            raise FileNotFoundError(f"Data folder '{self.data_folder}' not found.")
        
        for file_name in os.listdir(self.data_folder):
            if file_name.endswith('.xlsx') or file_name.endswith('.xls') or file_name.endswith('.csv'):
                return os.path.join(self.data_folder, file_name)
        
        print("No Excel file found in data folder.")

         
    def load_file(self):
        try:
            if self.file_path.endswith('csv'):
                self.dataframe = pd.read_csv(self.file_path)
            elif self.file_path.endswith('.xlsx') or self.file_path.endswith('.xls'):
                self.dataframe = pd.read_excel(self.file_path)

            print(f"✅ Successfully loaded: {self.file_path}")
        except Exception as e:
            print(f"❌ Error loading file: {e}")

    def get_all_data(self):
        if self.dataframe is not None:
            return self.dataframe
        else:
            print("⚠️ No data loaded. Please call load_file() first.")
            return None

    def get_column(self,  dataframe,column_name: str = "Email"):
        if dataframe is not None:
            if column_name in dataframe.columns:
                return dataframe[column_name]
            else:
                print(f"⚠️ Column '{column_name}' not found.")
                return None
        else:
            print("⚠️ No data loaded. Please call load_file() first.")
            return None

    def get_row(self, index):
        if self.dataframe is not None:
            if 0 <= index < len(self.dataframe):
                return self.dataframe.iloc[index]
            else:
                print(f"⚠️ Index {index} is out of range.")
                return None
        else:
            print("⚠️ No data loaded. Please call load_file() first.")
            return None

    def remove_duplicates(self, dataframe):
        cleaned_df = dataframe.drop_duplicates(subset=['Email'])
        return cleaned_df
        
    def retrieve_email(self, column_data):
        cleaned_emails = []

        for email in column_data:
            if email != '(No Email)' and pd.notna(email):
                cleaned_emails.append(email)
            
        return cleaned_emails 
    
    
    def process_file(self):
        """✨ Full process: load file, get all data, remove duplicates, and retrieve emails."""
        self.load_file()
        df = self.get_all_data()
        if df is None:
            print("❌ Failed to load data.")
            return None

        print(f"📄 Original entries: {len(df)}")
        cleaned_df = self.remove_duplicates(df)
        print(f"🧹 After removing duplicates: {len(cleaned_df)}")
        
        temp_emails = self.get_column(cleaned_df)
        emails = self.retrieve_email(temp_emails)
        if emails is not None:
            print(f"📧 Retrieved {len(emails)} emails.")
            return emails
        else:
            print("⚠️ No emails retrieved.")
            return None
            
    def clean_and_process_file(self, ctx):
        self.load_file()
        df = self.get_all_data()

        if df is None:
            print("❌ Failed to load data.")
            return None

        print(f"📄 Original entries: {len(df)}")

        # Step 1: Remove invalid emails
        df = df[df["Email"].notna()]
        df = df[df["Email"].str.strip() != "(No Email)"]

        print(f"🧼 After removing invalid emails: {len(df)}")

        # Step 2: Remove duplicates
        df = df.drop_duplicates(subset=["Email"])
        print(f"🧹 After removing duplicates: {len(df)}")



        try:
            # Step 3: Clean emails from the file
            df["Email_cleaned"] = df["Email"].str.strip().str.lower()
            email_set = set(df["Email_cleaned"])
            # Step 4: Get trainee records from Lark base
            table_id = os.getenv("TRAINEES_TABLE_ID")
            lark_records = ctx.base_manager.get_records(table_id=table_id)

            # Step 5: Extract en_names of matching emails
            trainees = []
            lark_emails = set()
            for record in lark_records:
                print(json.dumps(record.fields))
                email = record.fields.get("lark.Work email")
                if email:
                    lark_emails.add(email.strip().lower())

                
                # Extract 'en_name' from inside the 'lark' list
                lark_info = record.fields.get("lark", [])
                name = None
                if isinstance(lark_info, list) and lark_info:
                    name = lark_info[0].get("en_name")

                if email and name and email.strip().lower() in email_set:
                    trainees.append(name)

            df = df[df["Email_cleaned"].isin(lark_emails)]
            df.drop(columns=["Email_cleaned"], inplace=True)

            # ✅ Overwrite the file
            df.to_csv(self.file_path, index=False)
            print(f"🔍 Trainees matched: {len(trainees)}")


        except Exception as e:
            print(f"❌ Failed during processing: {e}")
            return None

        return trainees
