# v0.2.0

## New features

### Web App

- Built first draft of web app in Streamlit
![](assets/app_preview.png)
    - Display key metrics relating to model function (e.g. number of patients generated), and model outputs (e.g. money saved)
    - Allow setting of various parameters, including
        - Beds available in wawrd
        - Beds available in SDEC
        - SDEC and CTP operational hours
        - Random seed
- Added vidigi animation
- Added vidigi process map

### Automated Tests

- Added
    - backtest (test against a known 'good' set of results)
    - test for the same results being generated when the same paramaters and seed are used
    - test for **different** results being generated when the same parameters and a **different** seed are used

### Documentation

- Add numpydoc-style docstrings to all core model features
- Set up documentation site using mkdocs, mkdocs-material and mkdocstrings
    - Set up automatic building and publishing of site with GitHub action
    - Added .nojekyll file to ensure GitHub doesn't try to post-process the built site
- Built model flow diagram with Mermaid
    - this is available to view in the 'About' page of the Streamlit app
- Added first draft of STRESS DES model documentation
    - this can be viewed as part of the documentation site

## Enhancements

### Unavailability times for CTP and SDEC

- Adjusted how ctp_value and sdec_value are set up and used across the model, making it consistent across the script running and app methods and more consistent with how other variables are managed (i.e. using g class)
- Allow independent setting of the start hour for CTP and SDEC

### Inter-arrival time parameter

- Significantly adjusted how the inter-arrival time parameter is handled in the app to allow for demand adjustment via the web app interface
    - this more closely matches how inter-arrival time is defined in resources like HSMA's 'the little book of DES'
    - calculations were adjusted so that the average inter-arrival time passed through to the distribution did not change

### Other

- Switched from simpy resources to equivalent vidigi resources to support the recording of resource IDs in logs
- Added logging of model steps using the sim-tools trace function
    - rich logging of individual steps enhances debugging and understanding of the model for those who are less familiar with its structure
    - clock-time aware logging (i.e. using 'real' time with am/pm, rather than just sim-start relative time) used to make logs easier to interpret
- Recorded various additional attributes in patient object for easier referencing later
- Added patient objects to a list in the model, allowing for easy individual post-hoc querying of all recorded patient attributes
- Recorded various additional attributes in trial object for easier referencing later
- Added function to convert produced log into vidigi-style event log (`app/convert_event_log.py`)
- Enhanced controllable randomness and reproducibility
    - set up distinct random number streams per generator and activity using sim-tools distributions
    - set up uncorrelated random number streams using np.seedsequence
    - allowed user control of 'master' random seed used by np.seedsequence in g class and web frontend
- Switched various patient defaults from '0' to 'np.NaN' to help distinguish between cases of actual 0 and cases where the patient journey or run terminated before that value was populated for that patient.

## Bugfixes

- fixed typo in conditional check where it was accidentally looking at the sdec_value in the case where sdec_value was 100, where instead it should have been checking for ctp_value == 100 in that branch ([Click here to view commit, though note it's not showing the original code properly](https://github.com/Bergam0t/jw_hsma_des_stroke_project/commit/e5f653217ba40c3364cefcbad21dfb7951dc7eec))
- fixed bug in patient diagnosis allocation where certain diagnosis values above the ([Click here to view commit](https://github.com/Bergam0t/jw_hsma_des_stroke_project/commit/ccecec1b5c6c1239b43951265a8ef72dbf1cc319))
- ensured ward LOS was recorded in patient object for both thrombolysed and non-thrombolysed patients ([Click here to view commit](https://github.com/Bergam0t/jw_hsma_des_stroke_project/commit/874069fcf5081925f7f460f7caf2ba9f570b440b))

## Repository Admin and Structure

- Updated structure of code to package structure to support better long-term development and use of additional documentation tools
    - Model classes split into separate file to model running code
    - All code moved into src/stroke_ward_model
    - Classes split into separate files
    - Added pyproject.toml file
- Added "MARK" comments as markers to enable richer code minimap in core classes
- Updated gitignore with wildcards to make matching of additional results files more robust
- Added a minimal requirements.txt and environment.yml files to replace strongly specified win_environment and mac_environment folders
    - Added new requirements including streamlit, mkdocs, mkdocs-material, mkdocstrings, vidigi, pytest
- Added a separate requirements.txt file for web app
    - This removes the requirements that are not required for the web app, such as mkdocs and pytest
    - This will be picked up by Streamlit community cloud, and shortens the load time for container reloads

# v0.1.0

Initial model release.
