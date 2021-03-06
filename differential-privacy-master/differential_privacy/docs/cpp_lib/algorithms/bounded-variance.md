

<!-- This file is auto-generated. Do not edit. -->

# Bounded Variance

[`BoundedVariance`](https://github.com/google/differential-privacy/blob/master/differential_privacy/algorithms/bounded-variance.h) computes the
variance of values in a dataset, in a differentially private manner.

## Input & Output

`BoundedVariance` supports `int64` and `double` type input sets. When
successful, the returned [`Output`](https://github.com/google/differential-privacy/blob/master/differential_privacy/docs/cpp_lib/protos.md) message will
contain one element containing the differentially private variance. When bounds
are inferred, the `Output` additionally contains a `BoundingReport`. The
returned value is guaranteed to be non-negative, with a maximum possible value
of the maximum variance (bounded interval squared divided by four).

## Construction

`BoundedVariance` is a bounded algorithm. There are no additional parameters.
Information on how to construct a `BoundedVariance` is found in the
[bounded algorithm documentation](https://github.com/google/differential-privacy/blob/master/differential_privacy/docs/cpp_lib/algorithms/bounded-algorithm.md).
Below is a minimal construction example.

```
util::StatusOr<std::unique_ptr<BoundedVariance<int64>>> bounded_var =
            BoundedVariance<int64>::Builder.SetEpsilon(1)
                                           .SetLower(-10)
                                           .SetUpper(10)
                                           .Build();
```

## Use

`BoundedVariance` is an
[`Algorithm`](https://github.com/google/differential-privacy/blob/master/differential_privacy/docs/cpp_lib/algorithms/algorithm.md) and supports its full
API.

### Result Performance

For `BoundedVariance`, calling `Result` is an O(n) operation and requires O(1)
additional memory. Its performance is __not impacted__ by the provided iterator
category or by whether the data is sorted.
