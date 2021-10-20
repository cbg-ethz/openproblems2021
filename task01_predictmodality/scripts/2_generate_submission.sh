#!/bin/bash

set -e

# change these parameters if need be
PIPELINE_VERSION="1.2.0"

# helper functions

# get_script_dir: return the path of a bash file, following symlinks
function get_script_dir {
  SOURCE="$1"
  while [ -h "$SOURCE" ]; do
    DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"
    SOURCE="$(readlink "$SOURCE")"
    [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE"
  done
  cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd
}

# get_latest_release: get the version number of the latest release on git
function get_latest_release {
  curl --silent "https://api.github.com/repos/$1/releases/latest" | # Get latest release from GitHub api
    grep '"tag_name":' |                                            # Get tag line
    sed -E 's/.*"([^"]+)".*/\1/'                                    # Pluck JSON value
}
LATEST_RELEASE=`get_latest_release openproblems-bio/neurips2021_multimodal_viash`

# cd to root dir of starter kit
cd `get_script_dir ${BASH_SOURCE[0]}`/..

# This code was added by us. It's a hack.
echo ""
echo "######################################################################"
echo "##              Zipping the directory with the method code          ##"
echo "######################################################################"

rm -f method.zip
zip -r method.zip method

# End of our code. The rest of the file comes from the competition organizers.


# checking environment
scripts/0_sys_checks.sh

echo ""
echo "######################################################################"
echo "##              Build docker executable and container               ##"
echo "######################################################################"
bin/viash build config.vsh.yaml -o target/docker -p docker --setup cachedbuild \
  -c '.functionality.name := "method"'


echo ""
echo "######################################################################"
echo "##                      Build nextflow module                       ##"
echo "######################################################################"
# change the max time, max cpu and max memory usage to suit your needs.
bin/viash build config.vsh.yaml -o target/nextflow -p nextflow \
  -c '.functionality.name := "method"' \
  -c '.platforms[.type == "nextflow"].publish := true'


echo ""
echo "######################################################################"
echo "##                      Sync datasets from S3                       ##"
echo "######################################################################"

# don't sync data when testing the development starter kits
if [[ $PIPELINE_VERSION != "main_build" ]]; then
  VERSION_FILE="output/datasets/predict_modality/VERSION"

  # if the data is not found or is from a previous version starter kit,
  # sync from aws to local
  if [[ ! -f $VERSION_FILE || `cat $VERSION_FILE` != $PIPELINE_VERSION ]]; then
    mkdir -p output/datasets/predict_modality/

    # use aws cli if installed
    if command -v aws &> /dev/null; then
      aws s3 sync --no-sign-request \
        s3://openproblems-bio/public/phase1-data/predict_modality/ \
        output/datasets/predict_modality/
    # else use aws docker container instead
    else
      docker run \
        --user $(id -u):$(id -g) \
        --rm -it \
        -v $(pwd)/output:/output \
        amazon/aws-cli \
        s3 sync --no-sign-request \
        s3://openproblems-bio/public/phase1-data/predict_modality/ \
        /output/datasets/predict_modality/
    fi

    echo "$PIPELINE_VERSION" > $VERSION_FILE
  fi
fi

echo ""
echo "######################################################################"
echo "##            Generating submission files using nextflow            ##"
echo "######################################################################"

export NXF_VER=21.04.1

# removing previous output
[ -d output/predictions/predict_modality/ ] && rm -r output/predictions/predict_modality/

bin/nextflow \
  run openproblems-bio/neurips2021_multimodal_viash \
  -r $PIPELINE_VERSION \
  -main-script src/predict_modality/workflows/generate_submission/main.nf \
  --datasets 'output/datasets/predict_modality/**.h5ad' \
  --publishDir output/predictions/predict_modality/ \
  -resume \
  -latest \
  -c scripts/nextflow.config

echo ""
echo "######################################################################"
echo "##                      Creating submission zip                     ##"
echo "######################################################################"
[ -f submission.zip ] && rm submission.zip
zip -9 -r -q submission.zip . \
  --exclude=*.git* \
  --exclude=*.nextflow* \
  --exclude=*work* \
  --exclude=*.DS_Store* \
  --exclude=nextflow.config \
  --exclude=output/datasets/* \
  --exclude=bin/*

# print message
echo ""
echo "######################################################################"
echo "##                        Submission summary                        ##"
echo "######################################################################"
echo "Please upload your submission at the link below:"
echo "  https://eval.ai/web/challenges/challenge-page/1111/submission"
echo ""
echo "Or use the command below create a private submission:"
echo "> evalai challenge 1111 phase 2276 submit --file submission.zip --large --private"
echo ""
echo "Or this command to create a public one:"
echo "> evalai challenge 1111 phase 2276 submit --file submission.zip --large --public"
echo ""
echo "Good luck!"

if [ $PIPELINE_VERSION != $LATEST_RELEASE ]; then
  echo ""
  echo "######################################################################"
  echo "##                             WARNING                              ##"
  echo "######################################################################"
  echo "A newer version of this starter kit is available! Updating to the"
  echo "latest version is strongly recommended. See README.md for more info."
fi
