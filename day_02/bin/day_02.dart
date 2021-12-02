/*
https://adventofcode.com/2021/day/1
*/

import 'parts.dart';
import 'dart:io';

void main(List<String> arguments) {
  List<String> linesString = File('./input/raw_input.txt').readAsLinesSync();
  var partOne = PartOne(linesString);
  partOne.calculate();
  var solutionPartOne = partOne.solution;
  print('Solution of Part 1: $solutionPartOne\n -----------------------------');

  var partTwo = PartTwo(linesString);
  partTwo.calculate();
  var solutionPartTwo = partTwo.solution;
  print('Solution of Part 2: $solutionPartTwo\n -----------------------------');
}
