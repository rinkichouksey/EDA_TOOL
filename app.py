import pandas 
import streamlit as st 
from visualization import(
    histogram,
    box_plot,
    density_plot,
    violin_plot,
    scatter_plot,
    pair_plot,
    pie_chart,
     count_plot,
     line_chart,
     bar_chart,
     missing_bar,
     outlier_plot,
     correlation_heatmap
) 
from preprocessing import *  # * ka usse all ke liy use karte hai
from eda import *
from utils import *

st.set_page_config(
    page_title="Smart EDA Tool",
    layout="wide"
)
st.title("Smart EDA Tool")
st.markdown("---")

#sidebar
st.sidebar.title("Navigation")
uploaded_file = st.sidebar.file_uploader(
    "upload CSV /Excel",
    type=["csv","xlsx","xls"]   # Excel ka extention xlsx,  xls    full form Excel Spreadsheet 
)
if uploaded_file is None:
    st.info("upload a dataset to continue")
    st.stop()

df = load_data(uploaded_file)     #data_load funtion kisi bhi file me nahi banana hota hai 
if df is None:
    st.error("Unaable to read dataset")   # error detect ke liy use karte hai 
    st.stop()

working_df = df.copy()
with st.expander("file Details",expanded=False):
    details=get_file_details(uploaded_file)
    st.write(details) # write detail likhne ka kamm karta hai 

    st.header("Dataset Preview")
    rows = st.slider(
        "Rows",
        5,
        100,
        10
    )
    st.dataframe(
        working_df.head(rows),
        use_container_width=True     # space ke liy use karte hai 
    )

st.header("Dataset Overview")
show_dataset_metrics(working_df)
st.subheader("column summary")
st.dataframe(
    column_summary(working_df),
    use_container_width=True
)

info = overview(working_df)
c1 , c2 , c3 = st.columns(3)
c1.metric(
    "Rows",
    info["Rows"]
)
c2.metric(
    "columns",
    info["columns"]
)
c3.metric(
    "Memory(MB)",
    info["Memory usage (MB)"]
)
c4,c5,c6 = st.coulumn(3)
c4.metric(
    "Missing cells",
    info["Missing cells"]
)
c5.metric(
    "Duplicate Rows",
    info["Duplicate Rows"]
)
c6.metric(
    "Total cells",
    info["Total cells"]
)
# jab koi specific data show karna hai to as(astype(str)) ka use karte hai 
st.header("Data types")
datatype_df = pd.DataFrame({
    "column":working_df.columns,
    "Datatypes":working_df.dtypes.astype(str)
})

st.dataframe(
    datatype_df,
    use_container_width=True
)

st.header("Statistical Summary")
st.dataframe(
    describe_dataset(working_df),
    use_container_width=True
)

st.header("Numeric Summary")
num_summary = numeric_summary(working_df)
if not num_summary.empty:
    st.dataframe(
        num_summary,
        use_container_width=True
    )
else:
    st.warning("No Numeric Columns Found")

st.header("Categorical Summary")
cat_summary = categorical_summary(working_df)
if not cat_summary.empty:
    st.dataframe(
        cat_summary,
        use_container_width=True
    )
else:
    st.warning("No object datatype columns found")

st.header("Column Statistics")
all_columns = working_df.columns.tolist()
selected_column = st.selectbox(
    "Select Column",
    all_columns  
)

stats = column_statistics(
    working_df,
    selected_column
)
st.json(stats)

st.header("Missing Value Analysis")
missing_df = missing_summary(working_df)
st.dataframe(
    missing_df,
    use_container_width=True
)
fig = missing_bar(working_df)
if fig is not None:
    st.plotly_chart(
        fig,
        use_container_width=True
    )

#visualization parts 
st.markdown("----")
st.header("Data Visulization")
numeric_cols = numeric_columns(working_df)
categorical_cols = categorical_columns(working_df)
plot_type = st.selectbox(
    "Select Visualization",
    [
        "Histogram",
        "BOx plot",
        "Density  plot",
        "violin_plot",
        "Scatter plot",
        "Pair plot",
        "Pie Chart",
        "Count plot",
        "line_chart",    #time ke corresponding growth show karane ke liy 
        "Bar chart"
    ]
)
if plot_type =="HIstogram":
    column = st.selectbox(
        "Select Numeric column",
        numeric_cols,
        key="hist"
    ) 
    fig = histogram(working_df,column)
    st.plotly_chart(fig,use_container_width=True)
elif plot_type =="box_plot":
    column = st.selectbox(
         "Select Numeric column",
        numeric_cols,
        key="box"           
       )
    fig = box_plot(working_df,column)
    st.plotly_chart(fig,use_container_width=True)
elif plot_type =="Density  plot":
    column = st.selectbox(
         "Select Numeric column",
        numeric_cols,
        key="Density"           
       )
    fig = density_plot(working_df,column)
    st.plotly_chart(fig,use_container_width=True)
elif plot_type =="violin_plot":
    column = st.selectbox(
         "Select Numeric column",
        numeric_cols,
        key="violin"           
       )
    fig = violin_plot(working_df,column)
    st.plotly_chart(fig,use_container_width=True)
elif plot_type =="Scatter Plot":
    col1,col2 = st.columns(2)
    x =col1.selectbox(
        "x Axis",
        numeric_cols,
        key="scatter"
    )   
    y =col2.selectbox(
        "Y Axis",
        numeric_cols,
        key = "scatter_y"
    )
    color = st.selectbox(
        "colour(optional)",
        [None]+ categorical_cols
    )
    if color == "None":
        color = None 
    fig = scatter_plot(
        working_df,
        x,
        y,
        color
    )
    st.plotly_chart(fig,use_container_width=True)
elif plot_type == "Pair plot":
    st.info("Generating Pair plot..")
    fig = pair_plot(working_df)
    if fig is not None:
        st.plotly_chart(
            fig,
            use_container_width=True
        )
    else:
        st.warning("At leat two numeric columns are required")
elif plot_type == "Pie Chart":
    column = st.selectbox(
        "select categorical column",
        categorical_cols,
        key="Pie"
    )
    fig = "Pie Chart"(working_df)
    st.plotly_chart(fig,use_container_width=True)
elif plot_type == "Count plot":
    column = st.selectbox(
        "select categorical column",
        categorical_cols,
        key="Count"
    )
    fig = "Count plot"(working_df,column)
    st.plotly_chart(fig,use_container_width=True)
elif plot_type ==  "line_chart":
    col1,col2 = st.columns(2)
    x = col1.selectbox(
        "X Axis",
        working_df.columns,
        key=  "line_x"
    )
    y = col2.selectbox(
            "Y Axis,",
            working_df.columns,
            key=  "line_y"
    )
    fig = line_chart(
        working_df,
        x,
        y,
    )
    st.plotly_chart(fig,use_container_width=True)
elif plot_type ==   "Bar chart":
     col1,col2 = st.columns(2)
     x = col1.selectbox(
         "X Axis",
         working_df.columns,
         key=  "line_x"
    )
     y = col2.selectbox(
             "Y Axis,",
             working_df.columns,
             key=  "line_y"
    )
     fig = bar_chart(
         working_df,
         x,
         y,
    )
st.plotly_chart(fig,use_container_width=True) 

#correlation method 
st.markdown("---")
st.header("Correlation Analysis")
method = st.radio(
    "Correlation method",
    [
        "pearson",
        "spearman"
    ],
    horizontal=True
)
corr_fig = correlation_heatmap(
    working_df,
    method
)
if corr_fig is not None:
    st.plotly_chart(fig,use_container_width=True) 

 # outlier analysis
st.markdown("---")
st.header("outlier Detection")
column = st.selectbox(
    "select numberic column",
    numeric_cols,
    key="outlier"
)
fig = outlier_plot(
    working_df,column
)
st.plotly_chart(fig,use_container_width=True) 
#data cleaning 
st.markdown("---")
st.header("Data Preprocessing")
preprocessed_df = working_df.copy()

tab1,tab2,tab3,tab4 = st.tabs([
    "Cleaning",
    "Encoding",
    "Scaling",
    "Download"
])
with tab1:
    st.subheader("Data Cleaning ")
    cleaning_option = st.selectbox(
        "select cleaning operation",
        [
            "Fill Missing Value",
            "Remove Missing Row",
            "Remove Missing Columns",
            "Remove Duplicates",
            "Drop Columns",
            "Rename Column",
            "Convert Datatypes" 
        ]
    ) 
    if cleaning_option == "Fill Missing Value":
        column = st.selectbox(
            "Column",
            preprocessed_df.columns
        )
        method = st.selectbox(
            "Method",[
            "mean",
            "mode",
            "constant"
            ]
        )
        value = None
        if method =="constant":
            value = st.text_input(
                "Constant Value"
            )
        if st.button("Apply FIll Missing"):
            preprocessed_df = fill_missing(
                preprocessed_df,
                column,
                method,
                value
            )
            st.success("Done")
            st.dataframe(preprocessed_df.head())
    elif cleaning_option ==  "Remove Missing Row":
        if st.button("Remove"):
            preprocessed_df = remove_missing_rows(preprocessed_df)
            st.success("Rows Removed")
            st.dataframe(preprocessed_df.head())
    elif cleaning_option == "Remove Missing Columns":
         if st.button("Remove"):
            preprocessed_df = remove_missing_columns(preprocessed_df)
            st.success("Columns Removed")
            st.dataframe(preprocessed_df.head())
    elif cleaning_option == "Remove Duplicates":
         if st.button("Remove Duplicates"):
            preprocessed_df = remove_missing_columns(preprocessed_df)
            st.success( "Duplicates Removed ")
            st.dataframe(preprocessed_df.head())
    elif cleaning_option == "Drop Columns":
        cols = st.multiselect(
            "Columns",
            preprocessed_df.columns
        )
        if st.button("Drop"):
            preprocessed_df = drop_columns(
                preprocessed_df,
                cols
            )
            st.success("Column Droped")
            st.dataframe(preprocessed_df.head())
    elif cleaning_option ==  "Rename Column":
        old = st.selectbox(
            "Old Name",
            preprocessed_df.columns
        )
        new = st.text_input(
            "New Name"
        )
        if st.button("Rename"):
            preprocessed_df = rename_column(
                preprocessed_df,
                old,
                new
            )
            st.success("Renamed sucessfully")
            st.dataframe(preprocessed_df.head())
    elif cleaning_option ==   "Convert Datatypes":
        col = st.selectbox(
            "column",
            preprocessed_df.columns
        )
        dtype = st.selectbox(
            "Datatype",
            [
                "int",
                "float",
                "str",
                "bool",
                "datetime"
            ]
        )
        if st.button("Conver"):
            preprocessed_df = convert_datatype(
                preprocessed_df,
                col,
                dtype
            )
            st.success("Datatype Change")
            st.dataframe(preprocessed_df.head())
st.markdown("---")

st.markdown(
    """
    <div style='text-align:center'>
    <h4 Smart EDA TOOL</h4>
    <p>Built with using Streamlit, Plotly & Python</p>
    </div>
    """,
    unsafe_allow_html=True
)





                                                


