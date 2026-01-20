# Discrete Event Simulation of a Stroke Unit - what impact do specialised stroke same day emergency care units and ct perfusion scanning have on stroke patient flow?

This repository contains a discrete event simulation of

This project was written as part of the sixth round of the [Health Service Modelling Associates (HSMA) Programme](https://www.hsma.co.uk).

## Contributors

The majority of the work in this repository has been undertaken by [jfwilliams4](https://github.com/jfwilliams4).

Additional tweaks, documentation creation and web app creation has been undertaken by [Bergam0t](https://github.com/Bergam0t).

## Data used for Parameterising the Model

This model is parameterised using data from

- the Sentinel Stroke National Audit Programme (SSNAP)
- locally collected data from Maidstone Hospital
- general research on stroke care

## Environment setup

Install the environment using `requirements.txt` or `environment.yml` (tested with Python 3.12.10), found in the `environment/` folder.

This should automatically install the model code. If you receive errors about `stroke_ward_model` not being found in the environment you created then run: `pip install -e .`

**Note:** Legacy environments are also available in `win_environment/` and `mac_environment/`, but it is recommended that you use those provided in `environment/`.

## Running the model

To run the model via a script, with prompts for input variables, run the file `scripts/run_stroke_admission_model.py`.

## Web App

It is possible to run the model via a script, but for easy access to model parameters and all results tables and outputs, it is recommended to use the web app interface.

The hosted web app is available at [stroke-des.streamlit.app/](https://stroke-des.streamlit.app/). If you are unable to install Python code locally, you can use this free hosted version of the app, though note it may run more slowly.

To run the web app locally, you will need to install a separate environment provided in the `app/` folder. This is a reduced environment used by the hosted version of the web app on Streamlit Community Cloud. It does not install `mkdocs`, `pytest`, and other packages needed only for wider repository tasks. This `app/` environment must be manually updated whenever changes are made to the files in `environment/`.

Once the environment is installed, open a terminal in the root of the repository and run:

```
streamlit run app/streamlit_app.py
```

## Changelog

Please note all changes made to the code in the file `docs/CHANGELOG.md`.


## Documentation

The documentation site is provided using mkdocs-material and mkdocstrings.

It can be accessed at [sammirosser.com/jw_hsma_des_stroke_project/](http://sammirosser.com/jw_hsma_des_stroke_project/)

### Updating the Documentation

The changelog will automatically be pulled into the documentation.

Additional pages can be written in markdown and placed into the docs folder.

You must then add them to the 'nav' section of the file `mkdocs.yml`, which is present in the root folder.

The pages for the key model classes are built automatically, and new attributes, parameters and methods will be added to the documentation automatically as long as they are documented in the docstrings. If you add new classes or functions which need to be documented, follow the pattern used in the `docs/g.md` file for your new class, making sure to add it to the 'nav' section as with any other page.

You can preview the docs with the command `mkdocs serve`.

However, all publishing of the site is handled by GitHub actions (.github/workflows/publish-docs.yml); you do not need to build the documentation locally for it to update.

### Setting Up the Documentation After Forking

**If you are forking this repository**, you will need to go to your repository settings, then to 'pages', and choose 'Deploy from a branch', then make sure it is set to 'gh-pages' '/(root)', then save your selection.

The provided GitHub actions workflow in the .github/workflows/publish-docs.yml file will then be able to publish the docs to your page.

You will also need to update the `site_url` and `repository_url` parameter in the `mkdocs.yml` to reflect their new paths.

If you are not using a custom domain, the site will follow the pattern `http://your-github-username.github.io/your-forked-repository-name`
