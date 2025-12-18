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

Install environment using requirements.txt

In that environment, run `python install . -e` to install the model code.

This environment has been tested with Python 3.12.10

Note that at present legacy environments are also available in win_environment and mac_environment. It is recommended that you use requirements.txt and the method above.

## Running the Web App locally

To run the web app locally, ensure you have installed the environment as above, then open a terminal in the root of the repository and run the command `streamlit run app/streamlit_app.py`.

It is recommended to run the command above rather than moving into the `app` directory and running the streamlit command from there.

## Updating the documentation

The documentation site is provided using mkdocs-material and mkdocstrings.

Additional pages can be written in markdown and placed into the docs folder.
You must then add them to the 'nav' section of the file `mkdocs.yml`, which is present in the root folder.

The pages for the key model classes are built automatically, and new attributes, parameters and methods will be added to the documentation automatically as long as they are documented in the docstrings. If you add new classes or functions which need to be documented, follow the pattern used in the `docs/g.md` file for your new class, making sure to add it to the 'nav' section as with any other page.

You can preview the docs with the command `mkdocs serve`.

However, all publishing of the site is handled by GitHub actions; you do not need to build the documentation locally for it to update.

**If you are forking this repository**, you will need to go to your repository settings, then to 'pages', and choose 'Deploy from a branch', then make sure it is set to 'gh-pages' '/(root)', then save your selection.
The provided GitHub actions workflow in the .github/workflows/publish-docs.yml file will then be able to publish the docs to your page.

You will also need to update the `site_url` and `repository_url` parameter in the `mkdocs.yml` to reflect their new paths.

If you are not using a custom domain, the site will follow the pattern `http://your-github-username.github.io/your-forked-repository-name`
