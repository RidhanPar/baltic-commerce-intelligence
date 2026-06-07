# Run with base R: Rscript r/experiment_analysis.R
assignments <- read.csv("data/raw/experiment_assignments.csv")
prospects <- read.csv("data/raw/prospects.csv")
orders <- read.csv("data/raw/orders.csv")

customer_margin <- aggregate(contribution_margin ~ prospect_id, orders, sum)
names(customer_margin)[2] <- "customer_margin"

outcome <- merge(assignments, prospects[c("prospect_id", "converted")], by = "prospect_id")
outcome <- merge(outcome, customer_margin, by = "prospect_id", all.x = TRUE)
outcome$customer_margin[is.na(outcome$customer_margin)] <- 0

conversion_test <- prop.test(
  x = tapply(outcome$converted, outcome$treatment, sum),
  n = table(outcome$treatment),
  correct = FALSE
)
margin_test <- t.test(customer_margin ~ treatment, data = outcome)
srm_test <- chisq.test(table(outcome$treatment), p = c(0.5, 0.5))

cat("Conversion by arm:\n")
print(aggregate(converted ~ treatment, outcome, mean))
cat("\nConversion test:\n")
print(conversion_test)
cat("\nMargin per assigned prospect:\n")
print(aggregate(customer_margin ~ treatment, outcome, mean))
cat("\nMargin test:\n")
print(margin_test)
cat("\nSample-ratio mismatch test:\n")
print(srm_test)

