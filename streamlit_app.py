import streamlit as st
import requests
import plotly.express as px
import pandas as pd


API_URL = "http://localhost:8000"


st.set_page_config(page_title="Measurements & Scraper App", layout="centered")

st.title("📚 FastAPI + Streamlit App")


st.header("👤 Create User")
username = st.text_input("Username")

if st.button("Create User"):
    if username.strip() == "":
        st.error("Username cannot be empty.")
    else:
        response = requests.post(f"{API_URL}/users/", json={"name": username})
        if response.status_code == 200:
            st.success(f"User created! ID: {response.json()['id']}")
        else:
            st.error(f"Error: {response.text}")


st.header("➕ Add Measurement")

user_id = st.number_input("User ID", min_value=1, step=1)

st.write("Add measurement points (x,y):")

points_raw = st.text_area(
    "Enter points like:\n1,2\n3,4\n5,6",
    height=120
)

uploaded_file = st.file_uploader("Or upload a .txt file", type=["txt"])

if st.button("Submit Measurement"):
    try:
        points = []

        if uploaded_file is not None:
            content = uploaded_file.read().decode("utf-8")
            lines = content.splitlines()
        else:
            lines = points_raw.splitlines()

        for line in lines:
            if "," not in line:
                continue
            x, y = line.split(",")
            points.append({"x": float(x.strip()), "y": float(y.strip())})

        if not points:
            st.error("No valid points found. Make sure the format is 'x,y'.")
            st.stop()

        response = requests.post(
            f"{API_URL}/measurements/",
            params={"user_id": user_id},
            json={"points": points}
        )

        if response.status_code == 200:
            st.success(f"Measurement added! ID: {response.json()['id']}")
        else:
            st.error(f"Error: {response.text}")

    except Exception as e:
        st.error(f"Error: {str(e)}")


st.header("🔍 Get Measurement by ID")

measurement_id = st.number_input("Measurement ID", min_value=1, step=1, key="get_meas")

if st.button("Get Measurement"):
    response = requests.get(f"{API_URL}/measurements/{measurement_id}")

    if response.status_code == 200:
        meas = response.json()
        st.success("Measurement found!")
        st.json(meas)

        points = meas["points"]

        if len(points) > 0:
            x_vals = [p["x"] for p in points]
            y_vals = [p["y"] for p in points]

            fig = px.scatter(
                x=x_vals,
                y=y_vals,
                title=f"Measurement {measurement_id} - Points",
                labels={"x": "X Coordinate", "y": "Y Coordinate"},
            )

            fig.update_traces(marker=dict(size=10, color="red"))
            fig.update_layout(height=500)

            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No points to plot.")
    else:
        st.error("Measurement not found.")



st.header("📖 Book Scraper (books.toscrape.com)")

pages_to_scrape = st.number_input(
    "Number of pages to scrape (max 10 allowed in backend)", 
    min_value=1, 
    max_value=10, 
    value=1, 
    step=1, 
    key="pages_scrape"
)

if st.button("Scrape Books"):
    with st.spinner(f"Scraping {pages_to_scrape} pages..."):
        try:
            response = requests.get(f"{API_URL}/scrape_books/", params={"pages": pages_to_scrape}, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                books = data["books"]
                count = data["count"]
                
                st.success(f"Successfully scraped {count} books from {pages_to_scrape} pages!")
                
                df = pd.DataFrame(books)
                
                df['price_numeric'] = df['price']
                
                st.dataframe(df.style.highlight_max(axis=0, subset=['price_numeric']), use_container_width=True)
                
                if count > 0:
                    fig = px.histogram(
                        df, 
                        x="price_numeric", 
                        color="rating", 
                        title="Price Distribution by Rating",
                        labels={"price_numeric": "Price (£)", "rating": "Rating"}
                    )
                    st.plotly_chart(fig, use_container_width=True)

            elif response.status_code == 400:
                   st.error(f"Error: {response.json().get('detail', 'Bad Request')}")
            else:
                st.error(f"API Error ({response.status_code}): {response.text}")

        except requests.exceptions.ConnectionError:
            st.error(f"Connection Error: Could not connect to FastAPI at {API_URL}. Is the server running?")
        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")

st.markdown("---")