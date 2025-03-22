import streamlit as st
from datetime import datetime, date, time
from youtube_scraper import get_youtube_videos

st.title("Youtube Movie Explanation Videos Engagement Tracker")

st.subheader("Enter Start Date and Time")
start_date = st.date_input("Start Date", date.today())
start_time = st.time_input("Start Time", time(0, 0))
start_datetime = datetime.combine(start_date, start_time)

st.subheader("Enter End Date and Time")
end_date = st.date_input("End Date", date.today())
end_time = st.time_input("End Time", time(23, 59))
end_datetime = datetime.combine(end_date, end_time)

if st.button("Generate Report"):
    # Fixed query for movie explanation videos
    df = get_youtube_videos("movie explanation", max_results=50, start_dt=start_datetime, end_dt=end_datetime)

    if not df.empty:
        # Display only the video titles column
        video_titles = df[["Video Title"]]
        st.write("### Movie Explanation Videos Uploaded in the Given Time Frame:")
        st.dataframe(video_titles)
        st.download_button("Download CSV", video_titles.to_csv(index=False), "report.csv")
    else:
        st.warning("No videos found in the given time frame. Try a different range.")
