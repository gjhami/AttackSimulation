# cyberattack-simulation
An AnyLogic simulation model allowing users to quantitatively estimate the risk of cyber attacks to their organization, as well as the cost and efficacy of security controls.

## Warning
This project is currently under heavy development and is subject to major changes. When the code becomes more stable the AnyLogic model will be available as a standalone application which does not require an AnyLogic license to use and may be downloaded under Releases.

## Usage and Audience
This model is intended for small businesses/organizations without dedicated cybersecurity teams or experts who want to make more effective risk decisions while allocating a limited cybersecurity budget. The model will not represent every organization with pinpoint accuracy; it is meant to provide a useful tool accurate enough to improve decision making.

## Data Sources
Data related to control costs and efficacy mostly comes directly from vendors.
Data related to attacker efficacy and frequency comes from the [VERIS Community Database](https://github.com/vz-risk/VCDB) maintained by Verizon. This database contains the incident reports used to create the annual Verizon Breach Investigations Report [(DBIR)](https://www.verizon.com/business/resources/reports/dbir/).
Data related to attack costs is based on the [IBM Cost of a Data Breach Report](https://www.ibm.com/security/data-breach).

## Limitations
The model makes several assumptions and compromises in the name of data availability and ease of use. Some of these are as follows:
- Assumptions are made about the user's network which the creators believe are representative of many small businesses. The model will be more accurate for networks which more closely resemble the one used in the model. Some customization of nodes and services is possible from the main page menu.
- The model assumes incident reports in the VCDB are accurate. Any data bias (underreporting, skew towards particular industries, etc) on threat actor efficacy and frequency is inherited from Verizon's corpus of breach data. Incident reports are verified by the VCDB maintainers, but the majority are self-reported or submitted by the security community.
- The model assumes accuracy of vendor estimates of control pricing and efficacy.
- The model assumes individual records conform to the average pricing of the record type. I.e., any given customer record containing health information is worth the average amount for a health information record.

## Simulations
 Simulation modeling allows us to represent the data in a meaningful way, and to make reasonable estimations of outcomes. The model can quickly run hundreds or thousands of iterations using minimal resources, and visually displays attack likelihoods. 
