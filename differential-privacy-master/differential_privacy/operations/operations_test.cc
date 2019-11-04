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

#include "differential_privacy/base/testing/status_matchers.h"
#include "gmock/gmock.h"
#include "gtest/gtest.h"
#include "differential_privacy/base/status.h"

#include <limits>

namespace differential_privacy {
namespace operations {
namespace {

constexpr char kDatafile[] =
"differential_privacy/example/animals_and_carrots.csv";

TEST(OperatorTest, TrueStatistics) {
  Operator op(kDatafile, 1);
  EXPECT_EQ(op.Mean(0, std::numeric_limits<double>::max()),
            op.Sum(0, std::numeric_limits<double>::max()) / op.Count(0, std::numeric_limits<double>::max()));
  EXPECT_EQ(op.Max(0, std::numeric_limits<double>::max()), 100);
  EXPECT_EQ(op.Min(0, std::numeric_limits<double>::max()), 0);
  EXPECT_EQ(op.Variance(0, std::numeric_limits<double>::max()),
            op.StandardDeviation(0, std::numeric_limits<double>::max()) *
            op.StandardDeviation(0, std::numeric_limits<double>::max()));
}

TEST(OperatorTest, TooLittleBudget) {
  Operator op(kDatafile, 1);
  EXPECT_EQ(op.PrivateCount(2, 0, std::numeric_limits<double>::max()).status().code(),
            base::StatusCode::kInvalidArgument);
  EXPECT_EQ(op.PrivateMax(2, 0, std::numeric_limits<double>::max()).status().code(),
            base::StatusCode::kInvalidArgument);
  EXPECT_EQ(op.PrivateMin(2, 0, std::numeric_limits<double>::max()).status().code(),
            base::StatusCode::kInvalidArgument);
  EXPECT_EQ(op.PrivateMean(2, 0, std::numeric_limits<double>::max()).status().code(),
            base::StatusCode::kInvalidArgument);
  EXPECT_EQ(op.PrivateSum(2, 0, std::numeric_limits<double>::max()).status().code(),
            base::StatusCode::kInvalidArgument);
  EXPECT_EQ(op.PrivateVariance(2, 0, std::numeric_limits<double>::max()).status().code(),
            base::StatusCode::kInvalidArgument);
  EXPECT_EQ(op.PrivateStandardDeviation(2, 0, std::numeric_limits<double>::max()).status().code(),
            base::StatusCode::kInvalidArgument);
}

TEST(OperatorTest, PrivacyBudget) {
  Operator op(kDatafile, 1);
  EXPECT_EQ(op.PrivacyBudget(), 1.0);
  EXPECT_OK(op.PrivateMax(.2, 0, std::numeric_limits<double>::max()));
  EXPECT_EQ(op.PrivacyBudget(), .8);
  EXPECT_OK(op.PrivateMax(.8, 0, std::numeric_limits<double>::max()));
  EXPECT_EQ(op.PrivacyBudget(), 0.0);
}

}  // namespace
}  // namespace operations
}  // namespace differential_privacy
