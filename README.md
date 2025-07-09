# ygt-ai

# Step to prepare labeled data
## 1. Prepare data for labeling team
- Download data from google drive to local path, for example: "./data/original_data/invoices/"
- Create or Update data_info.csv to monitor data (idx,code,folder_name,file_name,file_type,split,in_use)
- Preprocessing data (remove duplicates, divide data by categories (PDFs, Excel, Word, EML))
- Split data by batches
## 2. Labeling data and get the labeled data 
- Labeling data:
    + PDFs, Word for Document AI 
    + Excel, EML for Gemini 
- Merge data into a single directory, update data_info.csv
## 3. Benchmarking data
- Run benchmarking on new dataset to get accuracy, speed performance.

