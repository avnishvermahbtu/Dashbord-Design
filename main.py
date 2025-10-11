import streamlit as st 
import pandas as pd   
import plotly.express as px
import os
import warnings
warnings.filterwarnings('ignore')
# =============================
# CUSTOM FRONT PAGE BANNER
# =============================

st.markdown("""
    <div style="
        background: linear-gradient(90deg, #1e3c72, #2a5298);
        padding: 25px;
        border-radius: 10px;
        text-align: center;
        color: white;
        font-size: 28px;
        font-weight: bold;">
        ✨ Welcome to the SuperStore Interactive Analytics Dashboard ✨
    </div>
""", unsafe_allow_html=True)

st.write("")  # spacing

st.info("""
**How to Use This Dashboard:**
1️⃣ Upload your data file OR use default dataset  
2️⃣ Filter using Region / State / City from the sidebar  
3️⃣ Explore dynamic charts, KPIs & time-series trends  
4️⃣ Download reports instantly!  
""")

st.markdown("""
    <style>
        .main {
            background-color: #F8F9FA;
        }
    </style>
""", unsafe_allow_html=True)


# =============================
# SIDEBAR FILTERS (Enhanced)
# =============================

st.sidebar.markdown("""
    <h2 style='text-align:center; color:#4CAF50;'>🧭 Filters & Controls</h2>
    <hr style='margin:5px 0px;'>
""", unsafe_allow_html=True)

st.sidebar.info("Apply filters below to customize your dashboard view.")

# Optional Mode Switch
view_mode = st.sidebar.radio("Select View Mode:", ["📊 Overview Mode", "📈 Detailed Analysis"])

# Tum is_mode ke hisaab se kuch charts show/hide bhi kar sakte ho later!




# =============================
# DASHBOARD TITLE AND SETTINGS
# =============================

st.set_page_config(page_title="Superstore!!!",page_icon=":bar_chart",layout="wide")

st.title(":bar_chart: Sample SuperStore EDA")
st.markdown('<style>jiv.block-container{padding-top:lrem;}',unsafe_allow_html=True)  

# =============================
# FILE UPLOAD SECTION
# =============================

fl=st.file_uploader(":file_folder: Upload a file",type=(["css","txt","xlsx","xls"]))
if fl is not None:
    filename=fl.name
    st.write(filename)   
    df=pd.read_excel(filename)
else:
    os.chdir(r"C:\Users\verma\OneDrive\Desktop\Streamlit")
    df = pd.read_excel("Superstore.xlsx")
    
# =============================
# DATE FILTER SECTION
# =============================
    
col1,col2=st.columns((2))
df["Order Date"]=pd.to_datetime(df["Order Date"])


## Getting the min and max date
startdate=pd.to_datetime(df["Order Date"]).min()
enddate=pd.to_datetime(df["Order Date"]).max()

with col1:
      date1=pd.to_datetime(st.date_input("Start Date",startdate))
with col2:
        date2=pd.to_datetime(st.date_input("Start Date",enddate))  

df=df[(df["Order Date"]>=date1) & (df["Order Date"]<=date2)].copy() 

# =============================
# SIDEBAR FILTERS
# =============================

st.sidebar.header("Choose your filter: ")


## filter Region
region=st.sidebar.multiselect("Pick your Region",df["Region"].unique())     
if not region:
    df2=df.copy()
else:
    df2=df[df["Region"].isin(region)]   ###.isin(region) → check karta hai ki "Region" column ka value region list ke andar hai ya nahi 
    

## filter state
state=st.sidebar.multiselect("Pick your State",df2["State"].unique())  
if not state:
    df3=df2.copy()
else:
    df3=df2[df2["State"].isin(state)]   
    

## filter city
city=st.sidebar.multiselect("Pick your City",df3["City"].unique())

# Filtered data based on all selections          

if not region and not state and not city:
    filtered_df=df
elif not  state and not city:
    filtered_df=df[df["Region"].isin(region)]
elif not region and not city:
    filtered_df=df[df["City"].isin(city)]
elif state and city:
    filtered_df=df3[df["State"].isin(state) & df3["City"].isin(city)]
elif region and city:
    filtered_df=df3[df["Region"].isin(region)& df3["City"].isin(city)]
elif region and state:
    filtered_df=df3[df["Region"].isin(region) & df3["State"].isin(state)]   
elif city:
    filtered_df=df3[df3["City"].isin(city)]
else:
    filtered_df=df3[df3["Region"].isin(region)& df3["City".isin(city)] &df3["State"].isin(state)]
    
category_df=filtered_df.groupby(by=["Category"],as_index=False)["Sales"].sum()    


# =============================
# KPI SECTION
# =============================
total_sales = int(filtered_df["Sales"].sum())
total_profit = int(filtered_df["Profit"].sum())
total_quantity = int(filtered_df["Quantity"].sum())
total_orders = filtered_df["Order ID"].nunique()

st.markdown("### 📊 Key Performance Indicators")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("💰 Total Sales", f"${total_sales:,.0f}")
kpi2.metric("📦 Total Quantity", total_quantity)
kpi3.metric("💹 Total Profit", f"${total_profit:,.0f}")
kpi4.metric("🧾 Total Orders", total_orders)
st.markdown("---")  # adds a horizontal line

# =============================
# CATEGORY & REGION CHARTS
# =============================

category_df=filtered_df.groupby(by=["Category"],as_index=False)["Sales"].sum()    

with col1:
    st.subheader("Category wise Sales")
    fig=px.bar(category_df,x="Category",y="Sales",text=[f"${x:,.2f}".format(x) for x in category_df["Sales"]],template="seaborn")
    st.plotly_chart(
    fig,
    config={
        "displayModeBar": False,   # hides toolbar
        "responsive": True          # makes chart resize automatically
    },
    use_container_width=True       # this one is still allowed in Streamlit
)
   ## st.plotly_chart(fig,use_container_width=True,height=200)
    
with col2:
    st.subheader("Region wise Sales")
    fig=px.pie(filtered_df,values="Sales",names="Region",hole=0.5)
    fig.update_traces(text=filtered_df["Region"],textposition="outside")
    st.plotly_chart(fig,use_container_width=True)
   
   
# ==========================
# DOWNLOAD DATA
#===========================

cl1,cl2=st.columns(2)
with cl1:
    with st.expander("Category_ViewData"):
        st.write(category_df.style.background_gradient(cmap="Blues"))
        csv=category_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Data",data=csv,file_name="Category.csv",mime="text/csv",help="Click here to download the data as a CSV file")   
         
with cl2:
    with st.expander("Region_ViewData"):
        region=filtered_df.groupby(by="Region",as_index=False)["Sales"].sum()
        st.write(region.style.background_gradient(cmap="Oranges"))
        csv=region.to_csv(index=False).encode('utf-8')
        st.download_button("Download Data",data=csv,file_name="Region.csv",mime="text/csv",help="Click here to download the data as a CSV file") 

# =============================
# TIME SERIES ANALYSIS
# =============================
        
filtered_df["month_year"]=filtered_df["Order Date"].dt.to_period("M")
st.subheader("Time Series Analysis")

linechart=pd.DataFrame(filtered_df.groupby(filtered_df["month_year"].dt.strftime("%Y:%b"))["Sales"].sum()).reset_index()
fig2=px.line(linechart,x="month_year",y="Sales",labels={"Sales":"Amount"},height=500,width=1000,template="gridon")
st.plotly_chart(fig2,use_container_width=True)         
        
with st.expander("View Data of TimeSeries"):
    st.write(linechart.T.style.background_gradient(cmap="Blues"))
    csv=linechart.to_csv(index=False).encode("utf-8")  
    st.download_button("Download Data",data=csv,file_name="TimeSeries.csv",mime='text/csv')               

# =============================
# TREEMAP
# =============================

## Create a treem based on Region,category ,sub-Category

st.subheader("Hierarchical view of Sales using TreeMap")    
fig3=px.treemap(filtered_df,path=["Region","Category","Sub-Category"],values="Sales",hover_data=["Sales"],color="Sub-Category")
fig3.update_layout(width=800 ,height=650) 
st.plotly_chart(fig3,use_container_width=True)        
    
chart1,chart2=st.columns(2)
with chart1:
    st.subheader("Segment wise Sales")
    fig=px.pie(filtered_df,values="Sales",names="Segment",template="plotly_dark")
    fig.update_traces(text=filtered_df["Segment"],textposition="inside")        
    st.plotly_chart(fig,use_container_width=True)
    
with chart2:
    st.subheader("Category wise Sales")
    fig=px.pie(filtered_df,values="Sales",names="Category",template="gridon")
    fig.update_traces(text=filtered_df["Category"],textposition="inside")        
    st.plotly_chart(fig,use_container_width=True)    
    
import plotly.figure_factory as ff     
st.subheader(":point_right: Month wise Sub-Category Sales Summary")

with st.expander("Summary Table"):
        df_sample=df[0:5][["Region","State","City","Category","Sales","Profit","Quantity"]]
        fig=ff.create_table(df_sample,colorscale="Cividis")
        st.plotly_chart(fig,use_container_width=True)
        
        st.markdown("Month wise sub-Category Table")
        filtered_df["month"]=filtered_df["Order Date"].dt.month_name()
        sub_category_year=pd.pivot_table(data=filtered_df,values="Sales",index=["Sub-Category"],columns="month")
        st.write(sub_category_year.style.background_gradient(cmap="Blues"))
        
## Create a sctter plot

fig_scatter = px.scatter(
    filtered_df, 
    x="Sales", 
    y="Profit", 
    size="Quantity", 
    color="Category", 
    hover_name="Sub-Category",
    hover_data=["Region", "State", "City"],
    template="plotly_white"
)
fig_scatter.update_layout(title="Sales vs Profit Scatter by Category")
st.plotly_chart(fig_scatter, use_container_width=True)

   
## 
with st.expander("View Data"):
    st.write(filtered_df.iloc[:500,1:20:2].style.background_gradient(cmap="Oranges")) 
    
## Download original Dataset
csv=df.to_csv(index=False).encode('utf-8')
st.download_button("Download Data",data=csv,file_name="Data.csv",mime='text/csv')           


                      
      
    
    


      
    