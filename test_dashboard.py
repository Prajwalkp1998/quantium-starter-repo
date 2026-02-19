import pytest
from solution1 import app


# --------------------------------------------------
# Test 1 — Header is present
# --------------------------------------------------

def test_header_present(dash_duo):

    dash_duo.start_server(app)

    header = dash_duo.find_element("h1")

    assert "Soul Foods Pink Morsel Sales Visualiser" in header.text


# --------------------------------------------------
# Test 2 — Visualization (Graph) is present
# --------------------------------------------------

def test_graph_present(dash_duo):

    dash_duo.start_server(app)

    graph = dash_duo.find_element("#sales-chart")

    assert graph is not None


# --------------------------------------------------
# Test 3 — Region picker (RadioItems) is present
# --------------------------------------------------

def test_region_picker_present(dash_duo):

    dash_duo.start_server(app)

    radio = dash_duo.find_element("#region-radio")

    assert radio is not None
