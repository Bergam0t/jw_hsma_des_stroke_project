"""
App utilities
"""

from streamlit_extras.stylable_container import stylable_container


def iconMetricContainer(
    key, icon_unicode, css_style=None, icon_color="grey", family="filled",
    type="icons"
):
    """
    Create a CSS styled container that adds a Material icon to a Streamlit
    `st.metric` component.

    Adapted from:
    https://discuss.streamlit.io/t/adding-an-icon-to-a-st-metric-easily/59140

    Parameters
    ----------
    key : str
        Unique key for the component.
    iconUnicode : str
        Unicode code point for the Material Icon, (e.g., "e8b6" used as
        "\\e8b6"). You can find them here: https://fonts.google.com/icons.
    css_style : str, optional
        Additional CSS to apply.
    icon_color : str, optional
        CSS color for the icon. Defaults to "grey".
    family : str, optional
        Icon family to use when type = "icons". Should be either "filled" or
        "outline".
    type : str, optional
        Icon font type: either "icons" (Material Icons) or "symbols" (Material
        Symbols Outlined).

    Returns
    -------
    DeltaGenerator
        A stylable container. Elements can be add to the container using "with"
        or by calling methods directly on the returned object.
    """
    # Choose the correct font-family for the icon
    if (family == "filled") and (type == "icons"):
        font_family = "Material Icons"
    elif (family == "outline") and (type == "icons"):
        font_family = "Material Icons Outlined"
    elif type == "symbols":
        font_family = "Material Symbols Outlined"
    else:
        print("ERROR - Check Params for iconMetricContainer")
        font_family = "Material Icons"

    # Base CSS that injects the icon before the st.metric value
    css_style_icon = f"""
                    div[data-testid="stMetricValue"]>div::before
                    {{
                        font-family: {font_family};
                        content: "\{icon_unicode}";
                        vertical-align: -20%;
                        color: {icon_color};
                    }}
                    """

    # Optionally append user-provided extra CSS
    if css_style is not None:
        css_style_icon += f"\n{css_style}"

    # Create the stylable container with the assembled CSS
    iconMetric = stylable_container(key=key, css_styles=css_style_icon)
    return iconMetric


def read_file_contents(file_name):
    """
    Read the entire contents of a text file.

    Parameters
    ----------
    file_name : str
        Path to file.

    Returns:
    -------
    str
        File contents as a single string.
    """
    with open(file_name, encoding="utf-8") as f:
        return f.read()
