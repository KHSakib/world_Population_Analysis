import streamlit as st
import pandas as pd
import plotly.express as px

# Title of the app
st.title("Data Viewer with Population Filter and Visualization")

# Sidebar for file upload and filter
st.sidebar.header("Upload and Filter Dataset")
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type=["csv"])

# Layout for dataset and filtered table display
col1, col2 = st.columns(2)

if uploaded_file is not None:
    try:
        # Read the uploaded CSV file
        df = pd.read_csv(uploaded_file)
        
        # Ensure necessary columns exist
        required_columns = ["2022 Population", "Country/Territory", "CCA3", "Continent"]
        if not all(col in df.columns for col in required_columns):
            st.error(f"The dataset must contain the following columns: {', '.join(required_columns)}.")
        else:
            # Sidebar slider for filtering by population
            min_population = int(df["2022 Population"].min())
            max_population = int(df["2022 Population"].max())

            st.sidebar.write("### Filter by Population")
            population_filter = st.sidebar.slider(
                "Select Population Range:",
                min_value=min_population,
                max_value=max_population,
                value=(min_population, max_population),
            )

            # Apply filter
            filtered_df = df[
                (df["2022 Population"] >= population_filter[0]) &
                (df["2022 Population"] <= population_filter[1])
            ]

            # Display original dataset in the first column
            with col1:
                st.write("### Original Dataset Preview")
                st.dataframe(df)

            # Display filtered dataset in the second column
            with col2:
                st.write("### Filtered Dataset Preview")
                st.dataframe(filtered_df)

            # Visualization row
            #st.write("## Visualizations")
            plot_col1, plot_col2 = st.columns(2)

            # World Map Plot
            with plot_col1:
                #st.write("### World Map Plot")
                world_map_fig = px.choropleth(
                    filtered_df,
                    locations="CCA3",
                    color="2022 Population",
                    hover_name="Country/Territory",
                    title="World Population by Country (Filtered)",
                    color_continuous_scale="Viridis",
                )
                st.plotly_chart(world_map_fig, use_container_width=True)

            # Packed Bubble Plot
            with plot_col2:
                #st.write("### Packed Bubble Plot")
                bubble_fig = px.scatter(
                    filtered_df,
                    x="Continent",
                    y="2022 Population",
                    size="2022 Population",
                    color="Continent",
                    hover_name="Country/Territory",
                    title="Population by Continent (Filtered Bubble Plot)",
                    size_max=60,
                )
                st.plotly_chart(bubble_fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error loading file: {e}")
else:
    st.info("Please upload a CSV file using the sidebar.")
