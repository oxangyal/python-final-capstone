import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import altair as alt

st.set_page_config(page_title="⚾ MLB Dashboard", layout="wide")
st.title("⚾ MLB Baseball Stats Dashboard")

# Cached functions
@st.cache_data
def get_table_names():
    with sqlite3.connect("mlb_cleaned.db") as conn:
        tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)
    return tables["name"].tolist()

@st.cache_data
def load_data(table_name):
    with sqlite3.connect("mlb_cleaned.db") as conn:
        df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
    return df

# Sidebar: Table selection
st.sidebar.header("Filter Options")
tables = get_table_names()
selected_table = st.sidebar.selectbox("Choose a table", tables)
df = load_data(selected_table)

# Ensure the "Year" column is valid
if "Year" in df.columns:
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df = df.dropna(subset=["Year"])
    df["Year"] = df["Year"].astype(int)

# Filters
if "Year" in df.columns:
    min_year, max_year = int(df["Year"].min()), int(df["Year"].max())
    year_range = st.sidebar.slider("Select Year Range", min_year, max_year, (2000, max_year))
    df = df[(df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1])]

if "League" in df.columns:
    leagues = df["League"].dropna().unique().tolist()
    selected_leagues = st.sidebar.multiselect("🏆 Select League(s)", leagues, default=leagues)
    df = df[df["League"].isin(selected_leagues)]

numeric_cols = df.select_dtypes(include="number").columns.tolist()

# Data Preview
st.subheader(f"Table: `{selected_table}`")
st.write(f"Total rows: {len(df)} | Columns: {list(df.columns)}")
st.dataframe(df.head(20))

# Visualizations
st.subheader("Visualizations")

# Top players by selected metric
if "Player" in df.columns and numeric_cols:
    metric_col = st.selectbox("Choose a metric", numeric_cols)
    top_df = df.sort_values(by=metric_col, ascending=False).head(10)

    # Bar chart with Plotly
    fig_bar = px.bar(top_df, x="Player", y=metric_col, color="Team", title=f"Top 10 by {metric_col}")
    st.plotly_chart(fig_bar, use_container_width=True)

# Combined scatter plot
if "Player" in df.columns and len(numeric_cols) >= 2:
    col1 = st.selectbox("Compare:", numeric_cols, key="col1")
    col2 = st.selectbox("vs", [c for c in numeric_cols if c != col1], key="col2")
    scatter_fig = px.scatter(df, x=col1, y=col2, color="Team" if "Team" in df.columns else None,
                             hover_name="Player", title=f"{col1} vs {col2}")
    st.plotly_chart(scatter_fig, use_container_width=True)

# Line chart: Best metric per year
if "Year" in df.columns and "League" in df.columns and metric_col:
    st.subheader(f"Best {metric_col} Per Year")
    top_avgs = df.groupby("Year")[metric_col].max().reset_index()
    top_avgs["Year"] = top_avgs["Year"].astype(str)
    st.line_chart(top_avgs.set_index("Year"))

# Team frequency chart
if "Team" in df.columns:
    st.subheader("Most Frequent League Leaders by Team")
    team_counts_df = df["Team"].value_counts().nlargest(10).reset_index()
    team_counts_df.columns = ["Team", "Count"]
    if not team_counts_df.empty:
        bar_chart = alt.Chart(team_counts_df).mark_bar().encode(
            x=alt.X("Team:N", sort="-y"),
            y="Count:Q",
            color="Team:N"
        )
        st.altair_chart(bar_chart, use_container_width=True)
    else:
        st.info("No team data available for the selected filters.")

# Pie chart: Team share by average metric
if "Player" in df.columns and "Team" in df.columns and metric_col:
    st.subheader("Team Share by AVG (Top 10)")
    team_avg = df.groupby(["Player", "Team"], as_index=False)[metric_col].max()
    team_avg_grouped = team_avg.groupby("Team", as_index=False)[metric_col].mean().sort_values(by=metric_col, ascending=False).head(10)

    teams = team_avg_grouped["Team"].tolist()
    colors = [f"hsl({i*37%360}, 70%, 60%)" for i in range(len(teams))]

    pie_chart = alt.Chart(team_avg_grouped).mark_arc().encode(
        theta=alt.Theta(field=metric_col, type="quantitative"),
        color=alt.Color("Team:N", scale=alt.Scale(domain=teams, range=colors)),
        tooltip=["Team", metric_col]
    ).properties(width=600, height=600)

    st.altair_chart(pie_chart, use_container_width=True)

# Summary statistics
st.subheader("Summary Statistics")
st.write(df.describe())
