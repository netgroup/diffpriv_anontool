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

      std::string true_value;
      std::string priv_value;

   public:

      // Constructor
      Result(std::string real, std::string priv) {
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
  else {
    // Load data into the Operator.
    double epsilon, budget, lower, upper;
    CHECK(absl::SimpleAtod(argv[1], &epsilon));
    CHECK(absl::SimpleAtod(argv[2], &budget));
    CHECK(absl::SimpleAtod(argv[3], &lower));
    CHECK(absl::SimpleAtod(argv[4], &upper));
    Operator op(absl::GetFlag(FLAGS_DataFile), epsilon);
    std::ofstream file("/tmp/result.csv");
    if (file.is_open()) {
      // Create an object containing true and private max values
      std::string true_val = absl::StrFormat("%f", op.Max(lower, upper));
      std::string priv_val = absl::StrFormat("%f", GetValue<int>(op.PrivateMax(budget, lower, upper).ValueOrDie().elements(0).value()));
      Result res(true_val, priv_val);
      // Write true and private max values on an output file
      file << res;
      file.close();
      return 0;
    }
    else
      return 1;
  }
}
