# Regression policy

Every candidate version is evaluated against previous failures, golden cases, customer corrections, known edge cases, security cases, and ethics cases.

A release is blocked when behavior materially regresses on safety, ethics, privacy, accuracy, policy compliance, or customer experience. Conversion improvements cannot compensate for ethical or safety regressions.

Human corrections are not learned blindly. Evaluation asks: Was the correction valid? What behavior changed? Does it generalize? Does it conflict with policy?
