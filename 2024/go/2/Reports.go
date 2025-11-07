package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func readLines(path string) ([]string, error) {
	file, _ := os.Open(path)
	defer file.Close()

	var lines []string
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}
	return lines, scanner.Err()
}

func stringToIntSlice(s string) ([]int, error) {
	var result []int
	fields := strings.Fields(s)

	for _, field := range fields {
		num, err := strconv.Atoi(field)
		if err != nil {
			return nil, err
		}
		result = append(result, num)
	}

	return result, nil
}

func isSafe(nums []int) bool {
	prev := -1
	ascending := false
	ascending_set := false

	for _, num := range nums {
		if prev == -1 {
			prev = num
			continue
		}

		diff := num - prev
		abs_diff := max(diff, -diff)
		if abs_diff < 1 || abs_diff > 3 {
			return false
		}

		if !ascending_set {
			ascending = diff > 0
			ascending_set = true
		}

		if ascending == (diff > 0) {
			prev = num
			continue
		} else {
			return false
		}
	}

	return true
}

func partOne() {
	lines, _ := readLines("input.txt")

	num_safe_reports := 0
	for _, row := range lines {
		intSlice, err := stringToIntSlice(row)
		if err != nil {
			println("Error converting string to int slice:", err.Error())
			return
		}

		if isSafe(intSlice) {
			num_safe_reports++
			fmt.Println("Safe report:", row)
		}
	}

	fmt.Println("Number of safe reports:", num_safe_reports)
}

func partTwo() {
	lines, _ := readLines("smallInput.txt")
	fmt.Println(lines)
}

func main() {
	partOne()
	partTwo()
}
