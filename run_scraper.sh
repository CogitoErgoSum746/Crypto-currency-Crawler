#!/bin/bash

# Function to run Scrapy spider continuously
run_spider() {
    while true; do
        scrapy crawl template_spider
        sleep 5  # Adjust the sleep duration as needed
    done
}

# Run the spider continuously
run_spider