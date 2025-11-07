package main

import (
	"bufio"
	"fmt"
	"os"
	"sort"
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

func partOne() {
	lines, _ := readLines("input.txt")

	left := make([]int, 0)
	right := make([]int, 0)

	total_sum := 0
	for _, row := range lines {
		fields := strings.Fields(row)

		first, err := strconv.Atoi(fields[0])
		if err != nil {
			fmt.Printf("Error converting first field to int: %v\n", err)
			return
		}

		second, err := strconv.Atoi(fields[1])
		if err != nil {
			fmt.Printf("Error converting second field to int: %v\n", err)
			return
		}

		left = append(left, first)
		right = append(right, second)
	}

	sort.Ints(left)
	sort.Ints(right)

	for i := 0; i < len(left); i++ {
		diff := left[i] - right[i]
		if diff < 0 {
			diff = -diff
		}
		total_sum += diff
	}

	fmt.Print("Total sum of absolute differences: ", total_sum, "\n")
}

func partTwo() {
	lines, _ := readLines("input.txt")

	left := make([]int, 0)
	right := make(map[int]int, 0)

	for _, line := range lines {
		fields := strings.Fields(line)

		first, err := strconv.Atoi(fields[0])
		if err != nil {
			fmt.Printf("Error converting first field to int in line %d: %v\n", err)
			return
		}

		second, err := strconv.Atoi(fields[1])
		if err != nil {
			fmt.Printf("Error converting second field to int in line %d: %v\n", err)
			return
		}

		left = append(left, first)
		right[second] += 1
	}

	similarity_score := 0
	for _, num := range left {
		similarity_score += num * right[num]
	}

	fmt.Println(similarity_score)
}

func main() {
	partOne()
	partTwo()
}
