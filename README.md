[![Download_Counter](https://img.shields.io/github/downloads/gjhami/AttackSimulation/total.svg)]()
# AttackSimulation
An AnyLogic simulation model allowing users to quantitatively estimate the risk of cyber attacks to their organization, as well as the efficacy and total cost of security controls.

## Disclaimer
This project is currently under heavy development and is subject to major changes. When the code becomes more stable the AnyLogic model will be available as a standalone application which does not require an AnyLogic license to use and may be downloaded under [Releases](https://github.com/gjhami/AttackSimulation/releases).

## Usage and Audience
This model is intended for small businesses/organizations without dedicated cybersecurity teams, or anyone trying to make more informed risk decisions while allocating a limited cybersecurity budget. The model will not represent every organization with pinpoint accuracy; it is meant to provide a useful tool accurate enough to improve decision making.

"All models are wrong, but some are useful." -George E.P. Box 

## Data Sources
Data related to security control costs and efficacy come primarily from vendors.
Data related to threat actor effectiveness and frequency come from the [VERIS Community Database](https://github.com/vz-risk/VCDB) maintained by the Verizon Security Research Team. This corpus of incident reports is used to create the annual Verizon Breach Investigations Report [(DBIR)](https://www.verizon.com/business/resources/reports/dbir/).
Data related to monetary costs of breaches are based on the [IBM Cost of a Data Breach Report](https://www.ibm.com/security/data-breach).

## Simulations
 Simulation modeling allows us to represent the data in a meaningful way, and to make reasonable estimations of outcomes based on observed samples. The model can quickly run hundreds or thousands of iterations using minimal resources, and visually displays attack success likelihoods. User selection of threat actors they anticipate facing, as well as security controls to implement, accordingly impact attack success predictions.

## Limitations
The model makes several assumptions and compromises in the name of data availability and ease of use. Some of these are as follows:
- Assumptions are made about the user's network which the creators believe are representative of many small businesses. The model will be more accurate for networks which more closely resemble the one used in the model. Some customization of nodes and services (and their ordering) is possible from the main page menu.
- The model assumes incident reports in the VCDB are accurate. Any data bias (underreporting, skew towards particular industries, etc) on threat actor effectiveness and frequency is inherited from Verizon's corpus of breach data. Incident reports are verified by the VCDB maintainers, but the majority are self-reported or submitted by the security community.
- The model assumes accuracy of vendor estimates of control pricing and efficacy.
- The model assumes individual records conform to the average pricing of the record type. I.e., any given customer record containing health information is worth the average amount for a health information record.
