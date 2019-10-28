//
// Copyright 2019 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//

#include "differential_privacy/operations/operations.h"

#include <fstream>

#include "differential_privacy/algorithms/bounded-mean.h"
#include "differential_privacy/algorithms/bounded-sum.h"
#include "differential_privacy/algorithms/count.h"
#include "differential_privacy/algorithms/order-statistics.h"
#include "absl/strings/numbers.h"
#include "absl/strings/str_split.h"

namespace differential_privacy {
namespace example {

Operator::Operator(std::string data_filename, double epsilon)
    : epsilon_(epsilon) {
  std::ifstream file(data_filename);
  std::string line;
  while (getline(file, line)) {
    std::vector<std::string> key_and_value = absl::StrSplit(line, ',');
    CHECK_EQ(key_and_value.size(), 2);
    int count;
    CHECK(absl::SimpleAtod(key_and_value[1], &count));
    value_per_key_[key_and_value[0]] = count;
  }
}

double Operator::Sum() {
  double sum = 0.0;
  for (const auto& pair : value_per_key_) {
    sum += pair.second;
  }
  return sum;
}

double Operator::Mean() {
  return static_cast<double>(Sum()) / value_per_key_.size();
}

double Operator::Variance() {
  double count = 0.0;
  for (const auto& pair : value_per_key_) {
    count += (pair.second * pair.second);
  }
  variance = count/value_per_key_.size() - (Mean() * Mean());
  return variance;
}

int Operator::CountAbove(double limit) {
  int count = 0;
  for (const auto& pair : value_per_key_) {
    if (pair.second > limit) {
      ++count;
    }
  }
  return count;
}

double Operator::Max() {
  double max = 0;
  for (const auto& pair : value_per_key_) {
    max = std::max(pair.second, max);
  }
  return max;
}

double Operator::Min() {
  double min = 0;
  for (const auto& pair : value_per_key_) {
    min = std::min(pair.second, max);
  }
  return min;
}

base::StatusOr<Output> Operator::PrivateSum(double privacy_budget, double lower, double upper) {
  ASSIGN_OR_RETURN(std::unique_ptr<BoundedSum<double>> sum_algorithm,
                   BoundedSum<double>::Builder()
                       .SetEpsilon(epsilon_)
                       .SetLower(lower) // default = 0
                       .SetUpper(upper) // default = 150
                       .Build());
  for (const auto& pair : value_per_key_) {
    sum_algorithm->AddEntry(pair.second);
  }
  return sum_algorithm->PartialResult(privacy_budget);
}

base::StatusOr<Output> Operator::PrivateMean(double privacy_budget) {
  ASSIGN_OR_RETURN(std::unique_ptr<BoundedMean<double>> mean_algorithm,
                   BoundedMean<double>::Builder().SetEpsilon(epsilon_).Build());
  for (const auto& pair : value_per_key_) {
    mean_algorithm->AddEntry(pair.second);
  }
  return mean_algorithm->PartialResult(privacy_budget);
}

base::StatusOr<Output> Operator::PrivateVariance(double privacy_budget, double lower, double upper) {
  ASSIGN_OR_RETURN(std::unique_ptr<BoundedVariance<double>> variance_algorithm,
                   BoundedVariance<double>::Builder()
                       .SetEpsilon(epsilon_)
                       .SetLower(lower) // default = 0
                       .SetUpper(upper) // default = 150
                       .Build());
  for (const auto& pair : value_per_key_) {
    variance_algorithm->AddEntry(pair.second);
  }
  return variance_algorithm->PartialResult(privacy_budget);
}

base::StatusOr<Output> Operator::PrivateStandardDeviation(double privacy_budget, double lower, double upper) {
  ASSIGN_OR_RETURN(std::unique_ptr<BoundedStandardDeviation<double>> standard_deviation_algorithm,
                   BoundedStandardDeviation<double>::Builder()
                       .SetEpsilon(epsilon_)
                       .SetLower(lower) // default = 0
                       .SetUpper(upper) // default = 150
                       .Build());
  for (const auto& pair : value_per_key_) {
    standard_deviation_algorithm->AddEntry(pair.second);
  }
  return standard_deviation_algorithm->PartialResult(privacy_budget);
}

base::StatusOr<Output> Operator::PrivateCountAbove(double privacy_budget, double limit) {
  ASSIGN_OR_RETURN(std::unique_ptr<Count<std::string>> count_algorithm,
                   Count<std::string>::Builder().SetEpsilon(epsilon_).Build());
  for (const auto& pair : value_per_key_) {
    if (pair.second > limit) {
      count_algorithm->AddEntry(pair.first);
    }
  }
  return count_algorithm->PartialResult(privacy_budget);
}

base::StatusOr<Output> Operator::PrivateMax(double privacy_budget, double lower, double upper) {
  ASSIGN_OR_RETURN(std::unique_ptr<continuous::Max<double>> max_algorithm,
                   continuous::Max<double>::Builder()
                       .SetEpsilon(epsilon_)
                       .SetLower(lower) // default = 0
                       .SetUpper(upper) // default = 150
                       .Build());
  for (const auto& pair : value_per_key_) {
    max_algorithm->AddEntry(pair.second);
  }
  return max_algorithm->PartialResult(privacy_budget);
}

base::StatusOr<Output> Operator::PrivateMin(double privacy_budget, double lower, double upper) {
  ASSIGN_OR_RETURN(std::unique_ptr<continuous::Min<double>> min_algorithm,
                   continuous::Min<double>::Builder()
                       .SetEpsilon(epsilon_)
                       .SetLower(lower) // default = 0
                       .SetUpper(upper) // default = 150
                       .Build());
  for (const auto& pair : value_per_key_) {
    min_algorithm->AddEntry(pair.second);
  }
  return min_algorithm->PartialResult(privacy_budget);
}

}  // namespace example
}  // namespace differential_privacy
