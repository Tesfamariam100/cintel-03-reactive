import plotly.express as px
from shiny.express import input, ui
from shinywidgets import render_plotly
from shiny import reactive, render, req
import seaborn as sns
import pandas as pd
import palmerpenguins

# Load the Palmer Penguins dataset
penguins_df = palmerpenguins.load_penguins()

# Set the page title
ui.page_opts(title="Penguins Data Tesfamariam")

# Create a Shiny UI sidebar
with ui.sidebar(open="open"):
    ui.h2("Sidebar")
    ui.input_selectize("selected_attribute", 
                       "Select Attribute",
                       ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]
                      )
    ui.input_numeric("plotly_bin_count", "Plotly Bin Count", 10)
    ui.input_slider("seaborn_bin_count", "Seaborn Bin Count", 1, 100, 50)
    ui.input_checkbox_group("selected_species_list", "Select Species", 
                             ["Adelie", "Gentoo", "Chinstrap"],
                             selected=["Adelie"], inline=False)
    ui.hr()
    ui.a("My GitHub", href="https://github.com/Tesfamariam100/cintel-02-data", target="_blank")

# Display a DataTable and a Data Grid
with ui.layout_columns():
    with ui.card(full_screen=True):
        ui.h2("Penguin Data Table")
        @render.data_frame
        def penguins_datatable():
            return render.DataTable(filtered_data()) 

    with ui.card(full_screen=True):
        ui.h2("Penguin Data Grid")
        @render.data_frame
        def penguins_grid():
            return render.DataGrid(filtered_data())

# Create a layout for the graphs
with ui.layout_columns():
    with ui.card(full_screen=True):
        ui.card_header("Plotly Graphs: Species")
        with ui.navset_card_tab(id="tab"):
            with ui.nav_panel("Plotly Histogram"):
                @render_plotly
                def plotly_histogram():
                    return px.histogram(penguins_df, x="species", title="Plotly Histogram: Species")

            with ui.nav_panel("Seaborn Histogram"):
                @render.plot
                def seaborn_histogram():
                    return sns.histplot(penguins_df, x="species", kde=False)

            with ui.nav_panel("Plotly Scatterplot"):
                @render_plotly
                def plotly_scatterplot():
                    return px.scatter(penguins_df, x="flipper_length_mm", y="bill_length_mm", color="species", 
                                      title="Plotly Scatterplot: Species")

# Add a reactive calculation to filter the data
@reactive.calc
def filtered_data():
    return penguins_df
