import 'dart:io';

// part 1 method
class PartOne {
  /*
  --- Day 3: Binary Diagnostic ---

  The submarine has been making some odd creaking noises, so you ask it to produce a diagnostic report just in case.

  The diagnostic report (your puzzle input) consists of a list of binary numbers which, when decoded properly, can tell you many useful things about the conditions of the submarine. The first parameter to check is the power consumption.

  You need to use the binary numbers in the diagnostic report to generate two new binary numbers (called the gamma rate and the epsilon rate). The power consumption can then be found by multiplying the gamma rate by the epsilon rate.

  Each bit in the gamma rate can be determined by finding the most common bit in the corresponding position of all numbers in the diagnostic report. For example, given the following diagnostic report:

  00100
  11110
  10110
  10111
  10101
  01111
  00111
  11100
  10000
  11001
  00010
  01010

  Considering only the first bit of each number, there are five 0 bits and seven 1 bits. Since the most common bit is 1, the first bit of the gamma rate is 1.

  The most common second bit of the numbers in the diagnostic report is 0, so the second bit of the gamma rate is 0.

  The most common value of the third, fourth, and fifth bits are 1, 1, and 0, respectively, and so the final three bits of the gamma rate are 110.

  So, the gamma rate is the binary number 10110, or 22 in decimal.

  The epsilon rate is calculated in a similar way; rather than use the most common bit, the least common bit from each position is used. So, the epsilon rate is 01001, or 9 in decimal. Multiplying the gamma rate (22) by the epsilon rate (9) produces the power consumption, 198.

  Use the binary numbers in your diagnostic report to calculate the gamma rate and epsilon rate, then multiply them together. What is the power consumption of the submarine? (Be sure to represent your answer in decimal, not binary.)

  */
  dynamic solution;
  dynamic inputList;

  dynamic powerConsumptionList;
  dynamic powerConsumption; // gammaRate * epsilonRate
  dynamic gammaRate; // most common for each bit 1st to nth Bit
  dynamic epsilonRate; // inverse gammaRate

  // Constructor, with syntactic sugar for assignment to members.
  PartOne(this.inputList) {
    // Initialize variables
    gammaRate = 0;
    epsilonRate = 0;
    powerConsumptionList = [];
    // read lines into list
    for (var line in inputList) {
      powerConsumptionList.add(line);
    }
  }

  // Named constructor that forwards to the default one.
  PartOne.calculate(inputList) : this(inputList);

  // Method.
  void calculate() {
    var transRows = powerConsumptionList[0].length;
    var transCols = powerConsumptionList.length;
    List<List<String>> transMatrix = [];
    for (int i = 0; i < transRows; i++) {
      List<String> row = [];
      for (int j = 0; j < transCols; j++) {
        row.add(powerConsumptionList[j][i]);
      }
      transMatrix.add(row);
    }

    var gammaValueString = '';
    var epsilonValueString = '';
    for (var row in transMatrix) {
      var gammaOnes = 0;
      var gammaZeroes = 0;
      for (var number in row) {
        if (number == '1') {
          gammaOnes += 1;
        } else {
          gammaZeroes += 1;
        }
      }
      if (gammaOnes > gammaZeroes) {
        gammaValueString += '1';
        epsilonValueString += '0';
      } else {
        epsilonValueString += '1';
        gammaValueString += '0';
      }
    }
    gammaRate = binaryToDecimal(gammaValueString);
    epsilonRate = binaryToDecimal(epsilonValueString);
    solution = gammaRate * epsilonRate;
  }

  int binaryToDecimal(String binaryNumber) {
    int res = 0;
    int base = 1;
    var tempString = binaryNumber;

    for (var i = binaryNumber.length - 1; i >= 0; i--) {
      var tempNum = int.parse(tempString[i]);
      res += tempNum * base;
      base *= 2;
    }
    return res;
  }
}
