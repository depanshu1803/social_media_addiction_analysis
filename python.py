import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config("Social Media Addiction Dashboard",layout='wide')

@st.cache_data
def load_data():
    df = pd.read_csv('Students Social Media Addiction.csv')
    return df
df = load_data()

# Sidebar Filters
st.sidebar.header('🔍 Filters')

Location = st.sidebar.multiselect("Choose Country",
                                 options=df['Country'].unique(),
                                 default=df['Country'].unique())

Category = st.sidebar.selectbox("Choose Platform",["ALL"]+
                                list(df['Most_Used_Platform'].unique()))

Season = st.sidebar.multiselect("Select Academic Level", df['Academic_Level'].unique())

Frequency = st.sidebar.multiselect("Addiction Level",
                                  df['Addicted_Score'].unique())

# Filtering
df_filtered = df[
    (df['Country'].isin(Location)) &
    (df['Most_Used_Platform'].isin([Category]) if Category != "ALL" else True) &
    (df['Academic_Level'].isin(Season) if Season else True) &
    (df['Addicted_Score'].isin(Frequency) if Frequency else True)
]

st.title("📱 Social Media Addiction Dashboard")

if not df_filtered.empty:
    total_usage = df_filtered['Avg_Daily_Usage_Hours'].sum()
    avg_usage = df_filtered['Avg_Daily_Usage_Hours'].mean()
    unique_students = df_filtered['Student_ID'].nunique()
    Top_Location = df_filtered['Country'].value_counts().idxmax()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("⏱ Total Usage Hours", f"{total_usage:,.1f}")
    col2.metric("📊 Avg Usage", f"{avg_usage:.2f} hrs")
    col3.metric("👥 Students", unique_students)
    col4.metric("🌍 Top Country", Top_Location)

else:
    st.warning("No data found for selected filters")

# Graphs
col1,col2 = st.columns(2)

with col2:
    df_perf = df_filtered.groupby('Affects_Academic_Performance')['Avg_Daily_Usage_Hours'].mean().reset_index()
    df_perf.columns=['Performance Impact','Average Usage']

    fig_perf = px.bar(df_perf,
        x='Performance Impact',
        y='Average Usage',
        title='Impact on Academic Performance',
        template='plotly_white',
        color='Performance Impact')

    st.plotly_chart(fig_perf,use_container_width=True)

with col1:
    df_rel = df_filtered.groupby('Relationship_Status')['Avg_Daily_Usage_Hours'].sum().reset_index()
    fig_rel = px.pie(df_rel,
        names='Relationship_Status',
        values='Avg_Daily_Usage_Hours',
        title='Relationship vs Usage',
        hole=0.5)
    st.plotly_chart(fig_rel)

# Next row
col1,col2 = st.columns(2)



with col1:
    df_level = df_filtered.groupby('Academic_Level')['Avg_Daily_Usage_Hours'].sum().reset_index()
    fig_level = px.pie(df_level,
        names='Academic_Level',
        values='Avg_Daily_Usage_Hours',
        hole=0.5,
        title='Usage by Academic Level')
    st.plotly_chart(fig_level)

with col2:
    df_platform = df_filtered['Most_Used_Platform'].value_counts().reset_index().head(7)
    df_platform.columns =["Platform","Count"]
    fig_platform = px.bar(df_platform,
        x='Platform',
        y='Count',
        color='Platform',
        title='Top Platforms')
    st.plotly_chart(fig_platform)

# Second line
col1,col2,col3 = st.columns(3)

with col1:
    gender = df_filtered['Gender'].value_counts().reset_index()
    gender.columns =['Gender','Count']
    fig_gender = px.pie(gender,names='Gender',values='Count',hole=0.5,title='Gender Distribution')
    st.plotly_chart(fig_gender)

with col2:
    bins = [15,20,25,30]
    labels = ['15-20','21-25','26-30']
    df_filtered['Age group'] = pd.cut(df_filtered['Age'],bins=bins,labels=labels)

    df_age = df_filtered['Age group'].value_counts().reset_index()
    df_age.columns=['Age group','Count']

    fig_age = px.bar(df_age,x='Age group',y='Count',color='Age group',title='Age Distribution')
    st.plotly_chart(fig_age)

with col3:
    df_sleep = df_filtered.groupby('Sleep_Hours_Per_Night')['Avg_Daily_Usage_Hours'].sum().reset_index()
    fig_sleep = px.line(df_sleep,
        x='Sleep_Hours_Per_Night',
        y='Avg_Daily_Usage_Hours',
        markers=True,
        title='Usage vs Sleep')
    st.plotly_chart(fig_sleep)

# Last row
col1,col2 = st.columns(2)

with col1:
    df_mental = df_filtered.groupby('Mental_Health_Score')['Avg_Daily_Usage_Hours'].sum().reset_index()
    fig_mental = px.pie(df_mental,
        names='Mental_Health_Score',
        values='Avg_Daily_Usage_Hours',
        hole=0.5,
        title='Mental Health Impact')
    st.plotly_chart(fig_mental)

with col2:
    df_conflict = df_filtered.groupby('Conflicts_Over_Social_Media')['Avg_Daily_Usage_Hours'].sum().reset_index()
    fig_conflict = px.bar(df_conflict,
        x='Conflicts_Over_Social_Media',
        y='Avg_Daily_Usage_Hours',
        title='Conflicts vs Usage')
    st.plotly_chart(fig_conflict)

# Scatter Plot Section
st.subheader("📊 Usage vs Mental Health (Scatter Plot)")

st.subheader("📊 Usage vs Mental Health")

fig_scatter = px.scatter(
    df_filtered,
    x='Avg_Daily_Usage_Hours',
    y='Mental_Health_Score'
)

st.plotly_chart(fig_scatter, use_container_width=True)

st.subheader("filtered Data preview")
st.dataframe(df_filtered.head(50),use_container_width=True )

