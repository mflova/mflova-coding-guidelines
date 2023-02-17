# Gtest

## Asserts/Expects

You can use either `EXPECT_X` or `ASSERT_X`. The second one stops the execution if the
condition is false. Useful if it is useless to continue the tests if there is something
wrong first.

Examples: `EXPECT_EQ`, `EXPECT_GE`, `EXPECT_NE`...

## Test types

We can say there are 4 main tests (personal opinion):

### Normal ones

Just a normal test with its own setup and stuff.

```cpp
#include <gtest/gtest.h>

TEST(TestSuiteName, TestName) {
  ... test body ...
}
```

### Fixture ones

Used for common setup among tests. It is a class that must derive
from `::testing::Test` and defines a `SetUp` and `TearDown`. 

```cpp
class FixtureTest : public ::testing::Test {
 protected:
  int x = 0;

  void SetUp() override {
    x = 42;
  }

  void TearDown() override {
    x = 0;
  }
};

TEST_F(FixtureTest, Test1) {
  EXPECT_EQ(x, 42);
}
```

Important things to notice: In the test, `TEST` needs to be renamed to `TEST_F`. The
fist argument is then the name of the fixture.

### Multiple test fixtures

If you want to set up multiple fixtures, the only way is performing multiple inheritance.
Quick example:

```cpp
class Fixture1 : public ::testing::Test {
 protected:
  int x = 0;
};

class Fixture2 : public ::testing::Test {
 protected:
  double y = 0.0;
};

class CombinedFixture : public Fixture1, public Fixture2 {};
```

### Typed test ones

Typed tests allow you to write a single test that is instantiated for multiple types
(useful for testing templates). Example:

```cpp
#include <gtest/gtest.h>

template<typename T>
class MyTest : public ::testing::Test {};

typedef ::testing::Types<int, float, double> MyTypes;
TYPED_TEST_CASE(MyTest, MyTypes);

TYPED_TEST(MyTest, Test) {
  TypeParam x = 0;
  EXPECT_EQ(x, 0);
}
```

Note that `MyTest` is still considered a fixture. With this setup, gtest will
automatically instantiate three tests: MyTest<int>, MyTest<float>, and MyTest<double>,
and run the test for each of these types.

### Value-Parametrized test ones:

Value-parameterized tests allow you to write a single test that is run multiple times
with different parameters

```cpp
#include <gtest/gtest.h>

class MyTest : public ::testing::TestWithParam<int> {};

TEST_P(MyTest, Test) {
  int x = GetParam();
  EXPECT_TRUE(x >= 0 && x <= 100);
}

INSTANTIATE_TEST_SUITE_P(MyInstance, MyTest, ::testing::Range(0, 100));
```

As more examples you can also use:
```cpp
INSTANTIATE_TEST_SUITE_P(MyInstance,
                         MyTest,
                         testing::Values(1, 2, 3));
```

### Multiple parameters

You can also parametrize multiple parameters by grouping them into a tuple and then
extracting these elementes with `std::get`.

```cpp
#include <gtest/gtest.h>
#include <tuple>

class MyTest : public ::testing::TestWithParam<std::tuple<int, int>> {};

TEST_P(MyTest, Test) {
  int x = std::get<0>(GetParam());
  int y = std::get<1>(GetParam());
  EXPECT_TRUE(x == y);
}

INSTANTIATE_TEST_SUITE_P(
        MyInstance,
        MyTest,
        ::testing::Values(
                std::make_tuple(1, 1),
                std::make_tuple(0, 0),
                std::make_tuple(4, 4,)));
```

## Mocking

As an example, you can mock a class with the following code:

```cpp
#include "gmock/gmock.h"  // Brings in gMock

class MockTurtle : public Turtle {
 public:
  ...
  MOCK_METHOD(void, PenUp, (), (override));
  MOCK_METHOD(void, PenDown, (), (override));
  MOCK_METHOD(void, Forward, (int distance), (override));
  MOCK_METHOD(void, Turn, (int degrees), (override));
  MOCK_METHOD(void, GoTo, (int x, int y), (override));
  MOCK_METHOD(int, GetX, (), (const, override));
  MOCK_METHOD(int, GetY, (), (const, override));
};
```

This is the simplest way, but it requires all these methods are `virtual`, since we are
inheriting from the class to be tested. If we want to mock classes with non-virtual
method, we will have to create a complete different class that mocks the signature of
the class to be tested. Next, you need a way to say that you want to use
normal class in production code, and use mocked class in tests
(see http://google.github.io/googletest/gmock_cook_book.html#mocking-class-templates)
In general, these mock implementations are recommended to be written in a separate `.h`
file.

These mock objects are mainly used to verify if they are called or not as expected.
As an example here, we are verifying whether `painter` makes use of `PenDown` member
function from the mocked object.

```cpp
TEST(PainterTest, CanDrawSomething) {
  MockTurtle turtle;                              // #2
  EXPECT_CALL(turtle, PenDown())                  // #3
      .Times(AtLeast(1));

  Painter painter(&turtle);                       // #4

  EXPECT_TRUE(painter.DrawCircle(0, 0, 10));      // #5
}
```

IMPORTANT: `EXPECT_CALL` has to be called before the function is called. Otherwise, the
behaviour is undefined.

General syntax:

```cpp
using ::testing::Return;

EXPECT_CALL(mock_object, method(matchers))
    .Times(cardinality)  // cardinality can be a number
    .WillOnce(action)  // action can be `Return(100)` for example.
    .WillRepeatedly(action);

// More specific:
EXPECT_CALL(turtle, GetX())
     .WillOnce(Return(100))
     .WillOnce(Return(200))
     .WillOnce(Return(300));

int n = 100;
EXPECT_CALL(turtle, GetX())
    .Times(4)
    .WillRepeatedly(Return(n++));
```
