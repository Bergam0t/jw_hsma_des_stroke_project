


# v0.2.0

## New features

- Built first draft of web app in Streamlit
![](assets/app_preview.png)
- Built model flow diagram with Mermaid
    - this is available to view in the 'About' page of the Streamlit app
- Set up documentation site using mkdocs, mkdocs-material and mkdocstrings
    - Set up automatic building and publishing of site with GitHub action
    - Added .nojekyll file to ensure GitHub doesn't try to post-process the built site
- Added first draft of STRESS DES model documentation
    - this can be viewed as part of the documentation site,

## Enhancements

- Recorded additional attributes in patient object
- Added patient objects to a list in the model, allowing for easy individual post-hoc querying of all recorded patient attributes
- Added logging of model steps using the sim-tools trace function
    - rich logging of individual steps enhances debugging and understanding of the model for those who are less familiar with its structure
- Adjusted how ctp_value and sdec_value are set up and used across the model, making it consistent across the script running and app methods and more consistent with how other variables are managed (i.e. using g class)
- Enhanced controllable randomness and reproducibility
    - set up distinct random number streams per generator and activity using sim-tools distributions
    - set up uncorrelated random number streams using np.seedsequence and
    - allowed user control of 'master' random seed used by np.seedsequence in g class and web frontend

## Bugfixes

- fixed typo in conditional check where it was accidentally looking at the sdec_value in the case where sdec_value was 100, where instead it should have been checking for ctp_value == 100 in that branch ([Click here to view commit, though note it's not showing the original code properly](https://github.com/Bergam0t/jw_hsma_des_stroke_project/commit/e5f653217ba40c3364cefcbad21dfb7951dc7eec))

## Repository Admin and Structure

- Updated structure of code to package structure
    - Model classes split into separate file to model running code
    - All code moved into src/stroke_ward_model
    - Added pyproject.toml file
- Added markers to enable richer code minimap in core classes
- Updated gitignore with wildcards to make matching of additional results files more robust
- Added a minimal requirements file
    - Added new requirements including streamlit, mkdocs, mkdocs-material, mkdocstrings,
- Added a separate requirements file for web app
    - This adds in automatic install of the


# v0.1.0

Initial model release.
