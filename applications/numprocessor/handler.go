package main

import (
	"context"
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"path/filepath"

	"github.com/aws/aws-lambda-go/lambda"
	"github.com/spf13/viper"
)

// Configuration represents the application's configuration
type Configuration struct {
	NumbersFile     string  `mapstructure:"numbers_file"`
	DefaultMultiplier float64 `mapstructure:"default_multiplier"`
}

// Request represents the Lambda function input
type Request struct {
	Operation string  `json:"operation"`
	Number    float64 `json:"number"`
}

// Response represents the Lambda function output
type Response struct {
	Result float64 `json:"result"`
	Error  string  `json:"error,omitempty"`
}

var (
	config Configuration
	numbers []float64
)

func init() {
	// Load configuration from file - demonstrates inefficient I/O during init
	viper.SetConfigName("config")
	viper.SetConfigType("yaml")
	viper.AddConfigPath(".")
	
	if err := viper.ReadInConfig(); err != nil {
		log.Printf("Warning: Could not read config file: %v", err)
		// Set default values
		viper.Set("numbers_file", "numbers.txt")
		viper.Set("default_multiplier", 2.0)
	}

	if err := viper.Unmarshal(&config); err != nil {
		log.Printf("Error unmarshaling config: %v", err)
		return
	}

	// Read numbers from file - demonstrates inefficient I/O during init
	if numbersData, err := ioutil.ReadFile(filepath.Join("/tmp", config.NumbersFile)); err == nil {
		// Create the numbers file with some sample data for testing
		if err := ioutil.WriteFile(filepath.Join("/tmp", config.NumbersFile), []byte("1.0\n2.0\n3.0\n4.0\n5.0"), 0644); err != nil {
			log.Printf("Error creating numbers file: %v", err)
		}
		
		fmt.Sscanf(string(numbersData), "%f\n%f\n%f\n%f\n%f", &numbers[0], &numbers[1], &numbers[2], &numbers[3], &numbers[4])
	} else {
		log.Printf("Error reading numbers file: %v", err)
		numbers = []float64{1.0, 2.0, 3.0, 4.0, 5.0} // Default values
	}
}

func handleRequest(ctx context.Context, req Request) (Response, error) {
	switch req.Operation {
	case "multiply":
		return Response{Result: req.Number * config.DefaultMultiplier}, nil
	case "average":
		if len(numbers) == 0 {
			return Response{Error: "no numbers available"}, nil
		}
		sum := 0.0
		for _, n := range numbers {
			sum += n
		}
		return Response{Result: sum / float64(len(numbers))}, nil
	default:
		return Response{Error: fmt.Sprintf("unknown operation: %s", req.Operation)}, nil
	}
}

func main() {
	lambda.Start(handleRequest)
}