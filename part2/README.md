# Assignment 1 Part 2

### Part 2 Overview:
This directory contains the contents for Assignment 1 Part 2. Included in this directory are `object.h`, `string.h`, `array.h`, and `test-array.cpp`. The Object, String, and Array classes are basic APIs that are to be fully implemented in a later assignment. The test file is a handful of tests that should pass once Object, String, and Array are fully implemented.

### Object:
Overview:
- A basic CwC class that is supposed to sit at the top of the object heirarchy

Contents:
- basic constructor and destructor
- virtual methods to be overriden
- hashing method to assist with equality

### String:
Overview:
- Subclass of Object
- A String class that is an immutable representation of char[]

Contents:
- basic constructors and destructors
- overriden methods from Object
- methods specific to String including concat and length

### Array:
Overview:
- Subclass of Object
- An Array class that is meant to handle general Objects as well as Strings

Contents:
- basic constructors and destructors
- overriden methods from Object
- methods specific to Array including clear, concat, get, index_of, length, pop, push, remove, replace