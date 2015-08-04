#!/bin/bash

# Forcing the modifiation of the LIVE tag
git tag -f LIVE

# Creation of another tag saying that it was deployed today
TAG=`date +DEPLOYED-%F/%H%M`

# Adding this tag
git tag $TAG

# Pushing those 2 tags to the GIT server
git push -f origin LIVE $TAG

echo "We are now deployed on $TAG"