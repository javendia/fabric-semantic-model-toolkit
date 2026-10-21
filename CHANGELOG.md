# Changelog

## 1.0.0

First stable release.

- Automatically generates date-based partitions (monthly, quarterly, or yearly) while preventing duplicates.
- Refreshes entire tables, specific partitions, or date ranges without processing the whole model.
- Recursively identifies related tables and can include them automatically in the refresh process.
- Provides an optional staged refresh strategy to reduce memory peaks, especially on more limited Microsoft Fabric capacities.
- Manages partition creation and refreshes independently or combines them in a single execution flow.
