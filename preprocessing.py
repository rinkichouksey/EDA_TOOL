import numpy as np
import pandas as pd 
from sklearn.preprocessing import (
     LabelEncoder,
     OneHotEncoder,
     StandardScaler,
     MinMaxScaler,
     RobustScaler,
)
# missing value handle 
def fill_missing(df,column,method="mean",value=None):
    """fill missing value in a column.
        method: 
        mean
        median
        mode
        constant
    """
    df = df.copy()
    if column not in df.columns:
        return df
    if method == "mean":
        if pd.api.types.is_numeric_dtype(df[column]):
            df[column] = df[column].fillna(df[column].mean())
    elif method == "median":
             if pd.api.types.is_numeric_dtype(df[column]):
                 df[column] = df[column].fillna(df[column].median())
    elif method == "mode":  
            mode = df[column].mode()
            if len(mode) > 0:
                df[column] = df[column].fillna(mode[0])
    elif method == "constant":
            df[column] = df[column].fillan(value)
    return df

# remove rows   
def remove_missing_rows(df):
     df = df.copy()
     return df.dropna()

# remove column
def remove_missing_columns(df):
     df = df.copy()
     return df.dropna(axis = 1)

# drop selected columns
def drop_columns(df,columns):
     df = df.copy()
     return df.drop(columns=columns)

# remove duplicates 
def remove_duplicates (df):
     df = df.copy()
     return df.drop_duplicates()

# rename columns
def rename_column(df,old_name,new_name):
     df = df.copy()
     if old_name not in df.columns:
          return df
     return df.rename(
          columns = {
               old_name:new_name
        }
    )


# change datatypes(type conversion ya type casting kahte hai )
def  convert_datatype(df,column,datatype):
     df = df.copy()
     try:
        if datatype == "int":
               df[column] = df[column].astype(int)
        elif datatype =="float":
               df[column] = df[column].astype(float)
        elif  datatype =="str":
               df[column] = df[column].astype(str)
        elif datatype =="bool":
               df[column] = df[column].astype(bool) 
        elif datatype == "datatime":
             df[column] = pd.to_datetime(df[column])  
     except Exception:
          pass
     return df 

# replace values
def replace_values(df, column, old_value, new_value):
     df = df.copy()
     df[column] = df[column].replace(old_value,new_value)
     return df

# remove negative value
def remove_negative_values(df,column):
     df = df.copy()
     if pd.api.types.is_numeric_dtype(df[column]):
          df = df[column] >=0
     return df

# remove empty string     (inplace = True) ka use parmanently change karne ke liy karte hai 
def remove_empty_strings(df):
     df = df.copy()
     df.replace("",np.nan,inplace = True)
     return df

# trim spaces 
def trim_spaces(df):
     df = df.copy()
     for col in df.select_dtypes(include="object"):
          df[col] = df[col].str.strip()
     return df 

# lowercase text
def lowercase_column(df):
     df = df.copy()
     object_cols = df.select_dtypes(include="object").columns
     for col in object_cols:
          df[col] = df[col].str.lower()
     return df 

# uppercase text
def uppercase_column(df):
     df = df.copy()
     object_cols = df.select_dtypes(include="object").columns
     for col in object_cols:
          df[col] = df[col].str.uper()
     return df

#title case function
def title_case_column(df):
     df = df.copy() 
     object_cols = df.select_dtypes(include="object").columns
     for col in object_cols:
          df[col] =df[col].str.title()
     return df 

# reset indexes 
def reset_index(df):
     return df.reset_index(drop = True)

# sort values 
def sort_dataframe(df,column,ascending =True):
     return df.sort_values(
          by = column,
          ascending = ascending
     )

#filter rows 
def filter_rows(df,column,value):
     return df[df[column] == value]

#label Encoder
def label_encoder(df,columns):
     df = df.copy()
     encoder  = LabelEncoder()
     for col in columns:
          if col in df.columns:
               df[col] = encoder.fit_transform(
                    df[col].astype(str)
               )
     return df 

# one hot encoder 
def one_hot_encode(df,columns):
     df = df.copy()
     df = pd.get_dummies(
          df,
          columns=columns,
          drop_first=False 
     )
     return df

# standard  scalar 
def standard_scale(df,columns):
     df = df.copy()
     scaler = StandardScaler()
     df[columns]= scaler.fit_transform(df[columns])
     return df 

#minmax scaler
def minmax_scaler(df,columns):
     df = df.copy()
     scaler = MinMaxScaler()
     df[columns]= scaler.fit_transform(df[columns])
     return df 

#robust scalar
def robust_scale(df,columns):
     df = df.copy()
     scaler = RobustScaler()
     df[columns]= scaler.fit_transform(df[columns])
     return df 

# fill all numaric 
def fill_all_numeric(df):
     df = df.copy()
     numaric = df.selct_dtypes(include=np.numric).column
     for col in numaric:
          df[col] = df[col].fillna(df[col].mean())
     return df 

# fill all categories
def fill_categorical(df):
     categorical = df.select_dtype(include = ["object","category"]).columns
     for col in categorical:
          mode = df[col].mode()
          if len(mode) > 0:
               df[col] = df[col].fillna(mode[0])
               return df 
                   
# pipeline 
def preprocess_dataset(df):
     df = remove_duplicates(df)
     df = remove_empty_strings(df)
     df = fill_all_numeric(df)
     df = fill_categorical(df)
     df = reset_index(df)
     return df 
    







     




     

    

         


      


     


            
    

