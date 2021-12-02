/*
https://adventofcode.com/2021/day/1
*/

import 'parts.dart';
import 'dart:io';

void main(List<String> arguments) {
  List<String> linesString = File('./input/raw_input.txt').readAsLinesSync();

  var partOne = PartOne(linesString);
  partOne.calculate();
  print(partOne.solution);
}
