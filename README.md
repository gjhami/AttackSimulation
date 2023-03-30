[![Download_Counter](https://img.shields.io/github/downloads/gjhami/AttackSimulation/total.svg)]()
# AttackSimulation
An AnyLogic simulation model allowing users to quantitatively estimate the risk of cyber attacks to their organization, as well as the efficacy and total cost of security controls. Stand-alone, cross-platform releases may be downloaded under [Releases](https://github.com/gjhami/AttackSimulation/releases).

## Usage and Audience
This model is intended for small businesses/organizations without dedicated cybersecurity teams, or anyone trying to make more informed risk decisions while allocating a limited cybersecurity budget. The model will not represent every organization with pinpoint accuracy; it is meant to provide a useful tool accurate enough to improve decision making.

"All models are wrong, but some are useful." -George E.P. Box

## Data Sources
Data related to security control costs and efficacy come primarily from vendors.
Data related to threat actor effectiveness and frequency come from the [VERIS Community Database](https://github.com/vz-risk/VCDB) maintained by the Verizon Security Research Team. This corpus of incident reports is used to create the annual Verizon Breach Investigations Report [(DBIR)](https://www.verizon.com/business/resources/reports/dbir/).
Data related to monetary costs of breaches are based on the [IBM Cost of a Data Breach Report](https://www.ibm.com/security/data-breach).

## Simulations
 Simulation modeling allows us to represent the data in a meaningful way, and to make reasonable estimations of outcomes based on observed samples. The model can quickly run hundreds or thousands of iterations using minimal resources, and visually displays attack success likelihoods. User selection of threat actors they anticipate facing, as well as security controls to implement, accordingly impact attack success predictions.
 
## Published Work
The initial model was published in the proceedings of proceedings of the 2022 IEEE International Symposium on Technologies for Homeland Security (HST). The paper is available at \[[IEEE Xplore](https://doi.org/10.1109/HST56032.2022.10024984)\] or \[[unpaywalled](https://docs.lib.purdue.edu/cit_articles/52)\]. The model was expanded and enhanced to include control pricing, budget allocation, and ROI in the thesis available \[[here](https://hammer.purdue.edu/articles/thesis/Making_the_Most_of_Limited_Cybersecurity_Budgets_with_AnyLogic_Modeling/20369418)\].

## Limitations
The model makes several assumptions and compromises in the name of data availability and ease of use. Some of these are as follows:
- Assumptions are made about the user's network which the creators believe are representative of many small businesses. The model will be more accurate for networks which more closely resemble the one used in the model. Some customization of nodes and services (and their ordering) is possible from the main page menu.
- The model assumes incident reports in the VCDB are accurate. Any data bias (underreporting, skew towards particular industries, etc) on threat actor effectiveness and frequency is inherited from Verizon's corpus of breach data. Incident reports are verified by the VCDB maintainers, but the majority are self-reported or submitted by the security community.
- The model assumes accuracy of vendor estimates of control pricing and efficacy.
- The model assumes individual records conform to the average pricing of the record type. I.e., any given customer record containing health information is worth the average amount for a health information record.

## Default Values and Useful Data Points
Note: All cost values are calculated based on the annual average of the 3-year total cost of ownership. All costs are in USD.

Control pricing, effectiveness, and variance
| Control Name                | Per Person /  Per Machine | Annual Cost (USD) | Effectiveness | Variance |
|-----------------------------|---------------------------|-------------------|---------------|----------|
| Intrusion Prevention System | N/A                       | Varies            | 0.9904        | 0.0144   |
| Antivirus                   | Yes                       | $127.20           | 0.9950        | 0        |
| Next Generation Firewall    | No                        | $7,453.00         | 0.9880        | 0        |
| Web Application Firewall    | No                        | $14,482.48        | 0.9985        | 0        |
| Email Filter                | Yes                       | $21.30-$313.20    | 0.9991        | 0        |
| Security Awareness Training | Yes                       | $17.00-30.50      | 0.5263        | 0        |

Estimates for budget, breach cost, and costs of variable cost controls based on business size
| Employee Count | Budget Amount | Breach Cost | IPS Cost  | Email Filter Cost | Security Training Cost (Per Person) |
|----------------|---------------|-------------|-----------|-------------------|-------------------------------------|
| 5              | $9,920.00     | $59,600.00  | $5,185.71 | $313.20           | $30.50                              |
| 25             | $49,600.00    | $298,000.00 | $5,288.55 | $1,127.52         | $30.50                              |
| 50             | $99,200.00    | $596,000.00 | $5,417.10 | $1,503.36         | $30.50                              |

## Disclaimer
The authors accept no responsibility for the accuracy of the model or real-world decisions based on its outputs.
