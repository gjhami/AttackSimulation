# cyberattack-simulation
An AnyLogic simulation allowing users to visually estimate the risk of cyber attacks as well as the cost and efficacy of controls.

## Warning
This project is currently under heavy development and is subject to major changes. When the code becomes more stable the AnyLogic model will be available as a standalone application which does not require an AnyLogic license to use and can be downloaded in Relases.

## Usage and Audience
This model is intended for small businesses without dedicated cybersecurity teams or experts who want to make more effective decsisions about how to allocate a limited cybersecurity budget. This model is not meant to be completely accurate for all businesses. It is only meant to provide a useful tool which is accurate enough to improve decision making.

## Data Sources
Data related to control costs and efficacy mostly comes directly from vendors.
Data related to attacker efficacy and frequency comes from the [VERIS Community Database](https://github.com/vz-risk/VCDB) provided by Verizon. This database contains the incident reports used to create the annual Verizon Breach Report.
Data related to attack costs is based on the IBM Cost of a Data Breach Report.

## Limitations
This model make several assumptions and compromises in the name of data availability and ease of use. Some of these are as follows:
- This model makes assumptions about the user's network which the creators believe are representative of many small businesses. The model will be more accurate for networks which more closely resemble the one used in the model.
- Ths model assumes incident reports in the VCDB are accurate. It should be noted these incident reports are verified by the maintainers, but still reported by the community or self-reported.
- This model assumes vendor estimates of control pricing and efficacy are accurate even though these metrics are self-reported.
- This model assumes individual records conform to the average pricing of the record type. Ex. any given customer record containing health information is worth the average amount for a health information record.
