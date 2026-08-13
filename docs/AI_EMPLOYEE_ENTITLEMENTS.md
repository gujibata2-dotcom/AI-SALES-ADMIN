# AI Employee Entitlements

Entitlements are resolved from the package catalog through `PackageEngine`; feature checks are not duplicated in UI/API policy.

Employee hiring checks package allowance, catalog availability, employee count and required permissions. The contract stores the effective package, permissions, quota and configuration so later package changes do not silently grant unrelated permissions.
