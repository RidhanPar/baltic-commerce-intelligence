# Validate a free-shipping-threshold experiment using intention-to-treat.
library(dplyr)
library(broom)

analyze_experiment <- function(assignments, orders) {
  outcome <- assignments |>
    left_join(
      orders |>
        group_by(customer_id) |>
        summarize(
          contribution_margin = sum(contribution_margin, na.rm = TRUE),
          ordered = as.integer(n() > 0),
          .groups = "drop"
        ),
      by = "customer_id"
    ) |>
    mutate(
      contribution_margin = coalesce(contribution_margin, 0),
      ordered = coalesce(ordered, 0)
    )

  margin_model <- lm(contribution_margin ~ treatment, data = outcome)
  conversion_model <- glm(ordered ~ treatment, data = outcome, family = binomial())

  list(
    sample_sizes = count(outcome, treatment),
    margin_result = tidy(margin_model, conf.int = TRUE),
    conversion_result = tidy(conversion_model, conf.int = TRUE, exponentiate = TRUE)
  )
}

