# Comparing 4 experiments
The 4 Experiments are as followed:
1. Without Undersampling and without dropout (v 1.a)
2. With undersampling but without dropout (v 1.b)
3. Without Undersampling but with dropout (v 2.a)
4. With undersampling and with dropout (v 2.b)

Uni-LSTM
- In 4 experiments, for Uni-LSTM model, all of them have the best AUC score of validation set on the base model (1.a - 75, 1.b - 78%, 2.a - 73, 2.b - 76).

Bi-LSTM
- In 4 experiments, for Bi-LSTM model, 2 of them have the best AUC score of validation set on the base model (1.b - 85%, 2.a - 78%). While for experiment 2 other experiments (1.a - 81.6% and 2.b - 72.8), the best AUC score of validation set are on the optimized model.

# Comparing Uni-LSTM and Bi-LSTM on 4 experiments
- The best possible scores of AUC for Uni-LSTM and Bi-LSTM are achieved in experiment 1.b (with undersampling but without dropout layer).
- The Bi-LSTM tends to have better performance according to Recall, Accuracy, and AUC score.
- Thus, the final model for deployment is Bi-LSTM.

# Re-check with Test Set
- After decided which model between Uni-LSTM and Bi-LSTM to choose as the final model, we want to make sure which Bi-LSTM is more reliable (stable) on the other set (test set). Now, we have to choose between Bi-LSTM from experiment 1.a and 1.b.
- AUC test set 1.a - 69.7%
- AUC test set 1.b - 64.8%
- AUC test set 2.a - 64.1%
- AUC test set 2.b - 69.5%

Bi-LSTM on experiment 1.a is more reliable as it has greater test set AUC. Although the Bi-LSTM 1.b have slightly better AUC (85% to 81.6%) it still ranges in 80%.

So, the final model for deployment is Bi-LSTM 1.a (without undersampling and without dropout layer).
