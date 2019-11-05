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

#include <iostream>
#include <fstream>

#include "differential_privacy/algorithms/confidence-interval.pb.h"
#include "differential_privacy/algorithms/util.h"
#include "differential_privacy/proto/data.pb.h"
#include "differential_privacy/proto/util.h"
#include "absl/flags/flag.h"
#include "absl/strings/numbers.h"
#include "absl/strings/str_format.h"
#include "differential_privacy/operations/operations.h"

using absl::PrintF;
using differential_privacy::BoundingReport;
using differential_privacy::ConfidenceInterval;
using differential_privacy::DefaultEpsilon;
using differential_privacy::GetValue;
using differential_privacy::Output;
using differential_privacy::operations::Operator;
using differential_privacy::base::StatusOr;

class Result {

   private:

      double true_value;
      std::string priv_value;

   public:

      // Constructors
      Result() {
         true_value = 0.0;
         priv_value = "";
      }

      Result(double real, std::string priv) {
         true_value = real;
         priv_value = priv;
      }

      friend std::ostream &operator<<(std::ostream &output, const Result &R) {
         output << R.true_value << "," << R.priv_value;
         return output;
      }

};

ABSL_FLAG(std::string, DataFile,
          "differential_privacy/operations/data.csv",
          "Path to the datafile where the data is stored.");

int main(int argc, char **argv) {
  if (argc < 5)
    return 1;
  // Load data into the Operator.
  double epsilon, budget, lower, upper;
  CHECK(absl::SimpleAtod(argv[2], &epsilon));
  CHECK(absl::SimpleAtod(argv[3], &budget));
  CHECK(absl::SimpleAtod(argv[4], &lower));
  CHECK(absl::SimpleAtod(argv[5], &upper));
  Operator op(absl::GetFlag(FLAGS_DataFile), epsilon);
  std::ofstream file("result.csv");
  if (file.is_open())
  {
    // Create an object containing true and private sums
    Result res(op.Sum(lower, upper), op.PrivateSum(budget, lower, upper).ValueOrDie().DebugString());
    // Write true and private sums on an output file
    file << res;
    file.close();
  }
  else
    return 1;
  return 0;
/*
  // Query for the mean with a bounding report.
  PrintF(
      "\nFarmer Fred catches on that the animals are giving him DP results. "
      "He asks for the mean number of carrots eaten, but this time, he wants "
      "some additional accuracy information to build his intuition.\n");
  PrintF("\nPrivacy budget remaining: %.2f\n", reporter.PrivacyBudget());
  PrintF("True mean: %.2f\n", reporter.Mean());
  StatusOr<Output> mean_status = reporter.PrivateMean(.25);
  if (!mean_status.ok()) {
    PrintF("Error obtaining mean: %s\n", mean_status.status().message());
    PrintF(
        "The animals were not able to get the private mean with the current "
        "privacy parameters. This is due to the small size of the dataset and "
        "random chance. Please re-run report_the_carrots to try again.\n");
  } else {
    Output mean_output = mean_status.ValueOrDie();
    BoundingReport report = mean_output.error_report().bounding_report();
    double mean = GetValue<double>(mean_output);
    int lower_bound = GetValue<int>(report.lower_bound());
    int upper_bound = GetValue<int>(report.upper_bound());
    double num_inputs = report.num_inputs();
    double num_outside = report.num_outside();
    PrintF("DP mean output:\n%s\n", mean_output.DebugString());
    PrintF(
        "The animals help Fred interpret the results. %.2f is the DP mean. "
        "Since no bounds were set for  the DP mean algorithm, bounds on the "
        "input data were automatically determined. Most of the data fell "
        "between [%d, %d]. Thus, these bounds were used to determine clamping "
        "and global sensitivity. In addition, around %.0f input values fell "
        "inside of these bounds, and around %.0f inputs fell outside of these "
        "bounds. num_inputs and num_outside are themselves DP counts.\n",
        mean, lower_bound, upper_bound, num_inputs, num_outside);
  }

  // Query for the count with a noise confidence interval.
  {
    PrintF(
        "\nFred wonders how many gluttons are in his zoo. How many animals ate "
        "over 90 carrots? And how accurate is the result?\n");
    PrintF("\nPrivacy budget remaining: %.2f\n", reporter.PrivacyBudget());
    Output count_output = reporter.PrivateCountAbove(.25, 90).ValueOrDie();
    int count = GetValue<int>(count_output);
    ConfidenceInterval ci =
        count_output.error_report().noise_confidence_interval();
    double confidence_level = ci.confidence_level();
    double lower_bound = ci.lower_bound();
    double upper_bound = ci.upper_bound();
    PrintF("True count: %d\n", reporter.CountAbove(90));
    PrintF("DP count output:\n%s\n", count_output.DebugString());
    PrintF(
        "The animals tell Fred that %d is the DP count. [%.2f, %.2f] is the "
        "%.2f confidence interval of the noise added to the count.\n",
        count, lower_bound, upper_bound, confidence_level);
  }

  // Query for the maximum.
  PrintF(
      "\n'And how gluttonous is the biggest glutton of them all?' Fred "
      "exclaims. He asks for the maximum number of carrots any animal has "
      "eaten.\n");
  PrintF("\nPrivacy budget remaining: %.2f\n", reporter.PrivacyBudget());
  PrintF("True max: %d\n", reporter.Max());
  PrintF("DP max:   %d\n",
         GetValue<int>(reporter.PrivateMax(.25).ValueOrDie()));

  // Refuse to query for the count of animals who didn't eat carrots.
  PrintF(
      "\nFred also wonders how many animals are not eating any carrots at "
      "all.\n");
  PrintF("\nPrivacy budget remaining: %.2f\n", reporter.PrivacyBudget());
  PrintF("Error querying for count: %s\n",
         reporter.PrivateCountAbove(.25, 0).status().message());
  PrintF(
      "The animals notice that the privacy budget is depleted. They refuse "
      "to answer any more of Fred's questions for risk of violating "
      "privacy.\n");*/
}
