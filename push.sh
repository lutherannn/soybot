#!/bin/bash

read -p "Message: " message

echo $message
git add --all
git commit -m "$message"
git push --all
