import streamlit as st
import json
import pandas as pd
import altair as alt

st.title("Topic Explorer: Author & Timeline Visualizations")

# File uploader for JSON
uploaded_file = st.file_uploader("Upload your topic JSON file", type="json")
if uploaded_file:
    # Load JSON data
    data = json.load(uploaded_file)
    # Flatten into DataFrame
    records = []
    for topic_str, msgs in data.items():
        topic = int(topic_str)
        for msg in msgs:
            records.append({
                "topic": topic,
                "author": msg.get("author", "unknown"),
                "timestamp": pd.to_datetime(msg.get("timestamp")),
                "content": msg.get("content", "")
            })
    df = pd.DataFrame(records)
    df['date'] = df['timestamp'].dt.date

    # Sidebar: topic selection
    topics = sorted(df['topic'].unique())
    selected_topics = st.sidebar.multiselect(
        "Select topics to display", topics, default=topics
    )

    for topic in selected_topics:
        st.header(f"Topic {topic}")
        df_topic = df[df['topic'] == topic]

        # Top authors bar chart
        author_counts = (
            df_topic['author']
            .value_counts()
            .reset_index(name='count')
            .rename(columns={'index': 'author'})
        )
        st.subheader("Top Authors")
        bar_chart = (
            alt.Chart(author_counts)
            .mark_bar()
            .encode(
                x=alt.X('count:Q', title='Message Count'),
                y=alt.Y('author:N', sort='-x', title='Author')
            )
        )
        st.altair_chart(bar_chart, use_container_width=True)

        # Timeline frequency line chart
        timeline = (
            df_topic.groupby('date')
            .size()
            .reset_index(name='count')
        )
        st.subheader("Timeline Frequency")
        line_chart = (
            alt.Chart(timeline)
            .mark_line(point=True)
            .encode(
                x=alt.X('date:T', title='Date'),
                y=alt.Y('count:Q', title='Number of Messages')
            )
        )
        st.altair_chart(line_chart, use_container_width=True)
else:
    st.info("Please upload a JSON file to begin visualizing your topics.")
