#pragma once
#include "object.h"

/**
 * An immutable String class representing a char*
 * author: chasebish */
class String : public Object {
public:

  /** VARIABLES */
  
  char* str_; // the string value stored
  size_t size_; // the length of the string

  /** CONSTRUCTORS & DESTRUCTORS **/

  /** Creates a String copying str */
  String(char* str) {}

  /** Creates a String copying str */
  String(const char* str) {}

  /** Copies a String copying the value from str */
  String(String* str) {}

  /** Clears String from memory */
  ~String() {}


  /** INHERITED METHODS **/

  /** Inherited from Object, generates a hash for a String */
  size_t hash_me_() {}

  /** Inherited from Object, checks equality between an String and an Object */
  bool equals(Object* obj) {}

  /** Inherited from Object, converts an String to a string */
  char* to_string() {}

  /** Inhertied from Object, prints a string representation of an String */
  void print() {}


  /** STRING METHODS **/

  /** Creates a new String by combining two existing Strings */
  String* concat(String* toAdd) {}

  /** Returns the current length of the String */
  size_t length() {}
};
