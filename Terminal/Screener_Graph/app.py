import streamlit as st
from multiapp import MultiApp
from apps import Graph, Screener, Trade, Portfolio,Pine # import your app modules here
st.set_page_config(layout="wide")
app = MultiApp()

# st.markdown("""
# # Multi-Page App
# This multi-page app is using the [streamlit-multiapps](https://github.com/upraneelnihar/streamlit-multiapps) framework developed by [Praneel Nihar](https://medium.com/@u.praneel.nihar). Also check out his [Medium article](https://medium.com/@u.praneel.nihar/building-multi-page-web-app-using-streamlit-7a40d55fa5b4).
# """)

# Add all your application here
app.add_app("Graph", Graph.app)
app.add_app("Screener", Screener.app)
app.add_app("Portfolio",Portfolio.app)
app.add_app("Pine to Python",Pine.app)
app.add_app("Trade",Trade.app)
# The main app
app.run()