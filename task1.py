####   project 1....  data cleaning
import pandas as pd
import re
df= pd.read_csv(r"C:\Users\PMLS\PycharmProjects\internship\archive\my_file (1).csv")
print(df.head())
print(df.info())
df.columns = df.columns.str.replace('\xa0', ' ')
df.columns= df.columns.str.strip()   #extra space ko remove kia
df.columns= df.columns.str.replace(" ","_")   #space ko _ mein change kia
print(df.columns)
df= df.drop(columns=["Ref."])    #reference column data analysis k liye useless hai...removed it
df["Artist"] = df["Artist"].apply(lambda x: re.sub(r'[^\x00-\x7F]+', '', str(x)))
#refernce wgera remove kiye hain yhan
def clean_tour_title(title):
    title= re.sub(r'\[+[^\]]*\]+',"", title )
    title= re.sub(r'[*#@$%^†‡]',"",  title)
    title = re.sub(r' +', ' ', title)
    title= title.strip()
    return title
df["Tour_title"]= df["Tour_title"].apply(clean_tour_title)
def clean_numbers(value):
    if pd.isna(value):
        return value
    return re.sub(r"\[.*?\]", "", str(value))
df["Rank"]= df["Rank"].apply(clean_numbers)
df["Peak"]= df["Peak"].apply(clean_numbers)
df["All_Time_Peak"]= df["All_Time_Peak"].apply(clean_numbers)
#ab jo string form mein hai data usko numeric mein convert krna hai
df["Rank"]= pd.to_numeric(df["Rank"], errors="coerce")
df["Peak"]= pd.to_numeric(df["Peak"], errors="coerce")
df["All_Time_Peak"]= pd.to_numeric(df["All_Time_Peak"], errors="coerce")
####  $symbol ya commas remove krny hain ab
cols= ["Actual_gross", "Adjusted_gross_(in_2022_dollars)", "Average_gross"]
for col in cols:
    df[col]= df[col].replace("[$,]", "", regex=True)
    df[col]= pd.to_numeric(df[col], errors="coerce")
## baki special symbols remove krny hain puri file mein sy
df= df.replace(r"[†‡]", "", regex=True)
###### years column ko clean krna hai is mein...range ko khtm krain gy
df["Year(s)"]= df["Year(s)"]. str.replace("–", "-") ##proper hyphen ka symbol use kia..201-202
df[["start_year", "End_year"]] = df["Year(s)"].str.split("-", expand=True )
df["start_year"]= pd.to_numeric(df["start_year"], errors="coerce")
df["End_year"] = pd.to_numeric(df["End_year"], errors="coerce")
 #######  handle missing values
print(df.isnull().sum())
 #### fill missing values
df["End_year"] = df["End_year"].fillna(df["start_year"])
df["Actual_gross"]= df["Actual_gross"].fillna(df["Actual_gross"]).median()
df["Peak"] = df["Peak"].fillna(df["Peak"]). median()
df["All_Time_Peak"] = df["All_Time_Peak"]. fillna(df["All_Time_Peak"]). median()
####  save the data
df.to_csv("final.csv", index=False)
########                     project 1 completed ...the end








