# v0.2.0

The main focus of this release is adding an interactive web app frontend to the model.

Where possible, the fundamental structure of the model code has been left unchanged.
Some unavoidable changes to support front end result display, reproducibility, or flexibility of parameter input.
Various bugfixes have also been introduced after discussion with the primary contributor.
Additional comments and docstrings have also been added for readability, and the code has been linted.

However, changes for aesthetic reasons, or where the change would reduce the readability/understandability
of the code for contributors with less experience in coding, have been avoided.

## New features

### Web App

- Built first draft of web app in Streamlit
![](assets/app_preview.png)
    - Display key metrics relating to model function (e.g. number of patients generated), and model outputs (e.g. money saved)
    - Allow setting of various parameters, including
        - Beds available in ward
        - Beds available in SDEC
        - SDEC and CTP operational hours
        - Random seed
    - Added vidigi animation
    - Added vidigi process maps
    - Added ward and SDEC occupancy plots
    - Added debugging plot for all patient attributes
    - Added about page with process diagram and placeholders for pathway and model FAQs.

### Automated Tests

- Added
    - backtest (test against a known 'good' set of results)
    - test for the same results being generated when the same paramaters and seed are used
    - test for **different** results being generated when the same parameters and a **different** seed are used

### Documentation

- Add numpydoc-style docstrings to all core model features
- Wrote comprehensive README
- Set up documentation site using mkdocs, mkdocs-material and mkdocstrings
    - Set up automatic building and publishing of site with GitHub action
    - Added .nojekyll file to ensure GitHub doesn't try to post-process the built site
- Built model flow diagram with Mermaid (docs/diagrams/pathway_diagram.mmd)
    - This is also available to view in the 'About' page of the Streamlit app
- Added first draft of STRESS DES model documentation
    - This can be viewed as part of the documentation site

## Enhancements

### Unavailability times for CTP and SDEC

- Adjusted how ctp_value and sdec_value are set up and used across the model, making it consistent across the script running and app methods and more consistent with how other variables are managed (i.e. using g class)
- Allow independent setting of the start hour for CTP and SDEC
    - Previously, the CTP and SDEC would always have their first period of availability commencing at sim time 0.
    - Sim time 0 has been reconceptualised to be midnight on the first simulated day.
    - Users can now provide separate offsets to separate the start time of CTP and SDEC
    - This also makes conversion of sim time to clock time more intuitive

### Inter-arrival time parameter

- Significantly adjusted how the inter-arrival time parameter is handled in the app to allow for demand adjustment via the web app interface
    - this more closely matches how inter-arrival time is defined in resources like HSMA's 'the little book of DES'
    - calculations were adjusted so that the average inter-arrival time passed through to the distribution did not change
- Allowed setting the start and end times of the arrival time periods
    - Previously, the start time of the first frequent arrival (daytime) period would be at sim time 0
    - Sim time 0 has been reconceptualised to be midnight on the first simulated day.
    - The start time and duration of the high/low arrival periods can now be set
    - This means that the arrival time periods can be decoupled from the CTP and SDEC availability times if desired

### Patient object

- Switched
    - float and integer defaults from 0 to np.NaN.
    - boolean defaults from False to None (with the exception of 'journey_complete').
    - This all helps to avoid masking subtle bugs arising from attributes not getting set, as well as the possibility of metric calculations being influenced by incorrect 0 values.
- Recorded various additional attributes in patient object for easier referencing later
- Split joing CT/CTP scanning attributes into separate attributes for easier debugging and pathway tracking

### Reproducibility

- Enhanced controllable randomness and reproducibility
    - Set up distinct random number streams per generator and activity using sim-tools distributions
    - Set up uncorrelated random number streams using np.seedsequence
    - Allowed user control of 'master' random seed used by np.seedsequence in g class and web frontend

### Animation and generated pathway diagrams

- Switched from simpy resources to equivalent vidigi resources to support the recording of resource IDs in logs
- Added function to convert produced log into vidigi-style event log (`app/convert_event_log.py`)

### Other

- Added logging of model steps using the sim-tools trace function
    - Rich logging of individual steps enhances debugging and understanding of the model for those who are less familiar with its structure
    - Clock-time aware logging (i.e. using 'real' time with am/pm, rather than just sim-start relative time) used to make logs easier to interpret
- Added patient objects to a list in the model, allowing for easy individual post-hoc querying of all recorded patient attributes
- Recorded various additional attributes in trial object for easier referencing later


## Bugfixes

- Fixed typo in conditional check where it was accidentally looking at the sdec_value in the case where sdec_value was 100, where instead it should have been checking for ctp_value == 100 in that branch ([Click here to view commit, though note it's not showing the original code properly](https://github.com/Bergam0t/jw_hsma_des_stroke_project/commit/e5f653217ba40c3364cefcbad21dfb7951dc7eec))
- Fixed bug in patient diagnosis allocation where a diagnosis between the stroke mimic and non-stroke threshold would not get allocated any diagnosis ([Click here to view commit](https://github.com/Bergam0t/jw_hsma_des_stroke_project/commit/ccecec1b5c6c1239b43951265a8ef72dbf1cc319))
    - note that this has also been added into the original repository
- Ensured ward LOS was recorded in patient object for both thrombolysed and non-thrombolysed patients ([Click here to view commit](https://github.com/Bergam0t/jw_hsma_des_stroke_project/commit/874069fcf5081925f7f460f7caf2ba9f570b440b))
- Swapped SDEC fullness check from <= to < (as previously may have allowed patients in if SDEC at capacity)
    - note that this has also been added into the original repository
- Adjust admission avoidance code to ensure that I and ICH patients never incorrectly jump from CT/CTP scan to discharge, and will always spend time in the SDEC at least

## Code Admin and Structure Changes

- Updated structure of code to package structure to support better long-term development and use of additional documentation tools
    - Model classes split into separate file to model running code
    - All code moved into src/stroke_ward_model
    - Classes split into separate files as some had become very long after adding docstrings
    - Added pyproject.toml file
- Added "MARK" comments as markers to enable richer code minimap in core classes.
    - These will appear if you are using the VSCode minimap
- Updated gitignore with wildcards to make matching of additional results files more robust
- Added a minimal requirements.txt and environment.yml files to replace strongly specified win_environment and mac_environment folders
    - Added new requirements including streamlit, mkdocs, mkdocs-material, mkdocstrings, vidigi, pytest
- Added a separate requirements.txt file for web app
    - This removes the requirements that are not required for the web app, such as mkdocs and pytest
    - This will be picked up by Streamlit community cloud, and shortens the load time for container reloads

# v.1.0.1



# v0.1.0

Initial model release.
