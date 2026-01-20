# Running the model locally

## Environment setup

Install environment using requirements.txt

In that environment, run `python install . -e` to install the model code.

This environment has been tested with Python 3.12.10

Note that at present legacy environments are also available in win_environment and mac_environment. It is recommended that you use requirements.txt and the method above.

## Script

To run the model via a script, with prompts for input variables, run the file `scripts/run_stroke_admission_model.py`.

## Web App

### Running the Web App locally

It is possible to run the model code via a script. However, for easy access to the model parameters and all model result tables and outputs, it's strongly recommended that you run the web app interface.

To run the web app locally, ensure you have installed the environment as above, then open a terminal in the root of the repository and run the command `streamlit run app/streamlit_app.py`.

It is recommended to run the command above rather than moving into the `app` directory and running the streamlit command from there.

### Accessing the web app on the web

If you are unable to install Python code, you can use the free hosted version of the app, though note that this will run more slowly.

[Click here to access the hosted version of the web app](app.md){.md-button}
