#pragma once
#include "object.h"

/**
 * An Array class to which elements can be added to and removed from.
 * author: chasebish */
class Array : public Object {
public:

  /** CONSTRUCTORS & DESTRUCTORS **/

  /** Creates an Array of desired size */
  Array(size_t array_size) {}

  /** Creates an Array of desired size */
  Array(const size_t array_size) {}

  /** Copies the contents of an already existing Array */
  Array(Array* copy_array) {}

  /** Clears Array from memory */
  ~Array() {}


  /** INHERITED METHODS **/

  /** Inherited from Object, generates a hash for an Array */
  size_t hash_me_() {}

  /** Inherited from Object, checks equality between an Array and an Object */
  bool equals(Object* obj) {}

  /** Inherited from Object, converts an Array to a string */
  char* to_string() {}

  /** Inhertied from Object, prints a string representation of an Array */
  void print() {}


  /** ARRAY METHODS **/

  /** Removes all elements from the Array */
  void clear() {}

  /** Adds an Array to existing contents */
  void concat(Array* toAdd) {}

  /** Gets an Object at the given index */
  Object* get(size_t index) {}

  /** Returns the index of the given Object, -1 if Object is not found */
  size_t index_of(Object* to_find) {}

  /** Returns the current length of the contents in an Array */
  size_t length() {}

  /** Removes the last Object of the Array, returns the removed Object */
  Object* pop() {}

  /** Adds an Object to the end of the Array, returns the new length */
  size_t push(Object* to_add) {}

  /** Removes an Object at the given index, returns removed Object */
  Object* remove(size_t index) {}

  /** Replaces an Object at the given index with the given Object, returns the replaced Object */
  Object* replace(size_t index, Object* new_value) {}
};
