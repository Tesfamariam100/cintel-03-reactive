import plotly.express as px
from shiny.express import input, ui
from shinywidgets import render_plotly
from shiny import reactive, render, req
import seaborn as sns
import pandas as pd
import palmerpenguins

# Use the built-in function to load the Palmer Penguins dataset
penguins_df = palmerpenguins.load_penguins()
ui.page_opts(title="Penguins Data Tesfamariam")

# Create a Shiny UI sidebar
with ui.sidebar(open="open"):
    # Add content to the sidebar
    ui.h2("Sidebar")
    # Use ui.input_selectize() to create a dropdown input to choose a column
    ui.input_selectize("selected_attribute", 
                       "Select Attribute",
                       ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]
                      )
    # Use ui.input_numeric() to create a numeric input for the number of Plotly histogram bins
    ui.input_numeric("plotly_bin_count", "Plotly Bin Count", 10)
    # Create a slider input for the number of Seaborn bins
    ui.input_slider("seaborn_bin_count", "Seaborn Bin Count", 1, 100, 50)
    # Create a checkbox group input to filter the species
    ui.input_checkbox_group("selected_species_list", "Select Species", 
                             ["Adelie", "Gentoo", "Chinstrap"],
                             selected=["Adelie"], inline=False)
    # Add a horizontal rule to the sidebar
    ui.hr()
    # Add a hyperlink to the sidebar
    ui.a("My GitHub", href="https://github.com/Tesfamariam100/cintel-02-data", target="_blank")

# Display a DataTable and a Data Grid
with ui.layout_columns():
    # DataTable showing all data
    @render.data_frame
    def penguins_datatable():
        return render.DataTable(penguins_df, width="70%") 

    # Data Grid showing all data
    @render.data_frame
    def penguins_grid():
        return render.DataGrid(penguins_df, width="70%")

# Create a layout for the graphs
with ui.layout_columns():
    # Create a card to contain the navigation tabs for graphs
    with ui.card(full_screen=True):
        ui.card_header("Plotly Graphs: Species")
        
        # Create tabs within the card
        with ui.navset_card_tab(id="tab"):
            # First tab for Plotly Histogram
            with ui.nav_panel("Plotly Histogram"):
                @render_plotly
                def plotly_histogram():
                    return px.histogram(penguins_df, x="species", title="Plotly Histogram: Species")

            # Second tab for Seaborn Histogram
            with ui.nav_panel("Seaborn Histogram"):
                @render.plot
                def seaborn_histogram():
                    return sns.histplot(penguins_df, x="species", kde=False)

            # Third tab for Plotly Scatterplot
            with ui.nav_panel("Plotly Scatterplot"):
                @render_plotly
                def plotly_scatterplot():
                    return px.scatter(penguins_df, x="flipper_length_mm", y="bill_length_mm", color="species", 
                                      title="Plotly Scatterplot: Species")
