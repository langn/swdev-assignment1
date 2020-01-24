#include <stdlib.h>
#include <stdio.h>
#include "array.h"
#include "string.h"

void FAIL(const char* m) {
  fprintf(stderr, "test %s failed\n", m);
  exit(1);
}
void OK(const char* m) { printf("test %s passed\n", m); }
void t_true(bool p, const char* m) { if (!p) FAIL(m); }
void t_false(bool p, const char* m) { if (p) FAIL(m); }

/** Tests Object equality */
void basic_object_test() {
  Object * x = new Object();
  Object * y = new Object();
  Object * z = new Object();

  t_true(x->equals(x), "1a");
  t_true(z->equals(z), "1b");
  t_false(x->equals(y), "1c");
  t_false(x->equals(y), "1d");

  delete z;
  delete y;
  delete x;

  OK("1");
}

/** Tests String equality */
void basic_string_test() {
  String * x = new String("x");
  String * x_copy = new String("x");
  String * y = new String("y");
  String * z = new String("z");

  t_true(x->equals(x_copy), "2a");
  t_false(x->equals(y), "2b");
  t_false(x->equals(z), "2b");

  delete z;
  delete y;
  delete x_copy;
  delete x;

  OK("2");
}

/** Tests pushing, popping, and length of Arrays */
void basic_array_test() {
  Object * x = new Object();
  Object * y = new Object();
  Object * z = new Object();
  Array * arr = new Array(10);

  arr->push(x);
  arr->push(y);
  arr->push(z);
  t_true(arr->length() == 3, "3a");
  arr->pop();
  t_true(arr->length() == 2, "3b");
  arr->clear();
  t_true(arr->length() == 0, "3c");

  delete arr;
  delete z;
  delete y;
  delete x;

  OK("3");
}

/** Tests more complex Array functions */
void complex_array_test() {
  Object * a = new Object();
  Object * b = new Object();
  Object * c = new Object();
  Object * x = new Object();
  Object * y = new Object();
  Object * z = new Object();
  Array * arr1 = new Array(10);
  Array * arr2 = new Array(10);

  arr1->push(a);
  arr1->push(b);
  arr1->push(c);
  arr2->push(x);
  arr2->push(y);
  arr2->push(z);
  Object * copy_of_a = arr1->get(0);
  t_true(copy_of_a->equals(a), "4a");
  arr1->concat(arr2);
  t_true(arr1->length() == 6, "4b");
  t_true(arr2->length() == 3, "4c");
  t_true(arr1->index_of(y) == 4, "4d");
  t_true(arr2->index_of(y) == 1, "4e");
  t_true(arr2->index_of(z) == 2, "4f");
  arr2->remove(2);
  t_true(arr2->index_of(z) == -1, "4g");
  arr2->replace(1, z);
  t_true(arr2->index_of(z) == 1, "4h");
  t_true(arr2->index_of(y) == -1, "4i");
  Array * copy_of_arr1 = new Array(arr1);
  t_true(copy_of_arr1->equals(arr1), "4j");

  delete arr2;
  delete arr1;
  delete z;
  delete y;
  delete x;
  delete c;
  delete b;
  delete a;

  OK("4");
}

int main() {
  basic_object_test();
  basic_string_test();
  basic_array_test();
  complex_array_test();
  exit(0);
}