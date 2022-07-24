import streamlit as st
import pandas as pd
import preprocessor,helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff


df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocessors(df, region_df)

st.sidebar.title("Olympics Analysis")
st.sidebar.image('https://www.kindpng.com/picc/m/631-6315896_olympic-lessons-for-better-health-olympic-logo-white.png')
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally','Overall Analysis','Country-Wise Analysis','Athlete Wise Analysis')
)

#st.dataframe(df)

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years,region = helper.country_year_list(df)


    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_region = st.sidebar.selectbox("Select Country", region)

    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_region)
    if selected_year == 'Overall' and selected_region == 'Overall':
        st.title("Overall Tally")
    if selected_year != 'Overall' and selected_region == 'Overall':
        st.title("Medal Tally in " + str(selected_year) + " Olympics")
    if selected_year == 'Overall' and selected_region != 'Overall':
        st.title(selected_region + " Overall Tally")
    if selected_year != 'Overall' and selected_region != 'Overall':
        st.title(selected_region  + "performance in " + str(selected_year) + " Olympics")

    st.table(medal_tally)


if user_menu == ('Overall Analysis'):
    editions = df['Year'].unique().shape[0] -1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    atheletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("Top Statistics")
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1,col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(atheletes)

    nations = helper.data_over_time(df,'region')
    fig = px.line(nations, x="Edition", y="region")
    st.title("Participating Nations Over The Years")
    st.plotly_chart(fig)

    events = helper.data_over_time(df,'Event')
    fig = px.line(events, x="Edition", y="Event")
    st.title("Events Over The Years")
    st.plotly_chart(fig)

    atheletes = helper.data_over_time(df, 'Name')
    fig = px.line(atheletes, x="Edition", y="Name")
    st.title("Athletes Over The Years")
    st.plotly_chart(fig)

    st.title("Number of Events over Time")
    fig,ax = plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    y = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
                annot=True)
    st.pyplot(fig)


    st.title("Most Successful Athlete")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    selected_sport = st.selectbox('Select a Sport',sport_list)
    x = helper.most_success(df,selected_sport)
    st.table(x)

if user_menu == 'Country-Wise Analysis':

    st.sidebar.title("Country-Wise Analysis")

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a Country',country_list)

    country_df = helper.year_wise_medal_tally(df,selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.title(selected_country + " Medal Tally over the Years")
    st.plotly_chart(fig)

    st.title(selected_country+" excels in following sports")
    pt = helper.country_win_heatmap(df,selected_country)
    fig,ax = plt.subplots(figsize=(20,20))
    ax = sns.heatmap(pt,annot = True)
    st.pyplot(fig)

    st.title("Top 10 Athletes of "+ selected_country)
    top10 = helper.most_success_country_wise(df,selected_country)
    st.table(top10)


if user_menu == 'Athlete Wise Analysis':
    ath = df.drop_duplicates(subset=['Name', 'region'])

    x1 = ath['Age'].dropna()
    x2 = ath[ath['Medal'] == 'Gold']['Age'].dropna()
    x3 = ath[ath['Medal'] == 'Silver']['Age'].dropna()
    x4 = ath[ath['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'], show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=950,height=600)
    st.title("Age Distribution")
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = ath[ath['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=900, height=600)
    st.title("Age Distribution wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title("Height vs Weight")

    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp = helper.weight_vs_height(df,selected_sport)
    fig,ax = plt.subplots()
    ax = sns.scatterplot(temp['Weight'],temp['Height'], hue=temp['Medal'],style = temp['Sex'],s=50)
    st.pyplot(fig)

    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=950, height=600)
    st.plotly_chart(fig)


